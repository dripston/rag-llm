import os
import json
import logging
from dotenv import load_dotenv
from pinecone import Pinecone
import requests
import time
from typing import Any, Dict, List, Optional

# Set up logging
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configuration
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
LLM_API_KEY = os.getenv("LLM_API_KEY")
SAMBANOVA_BASE_URL = os.getenv("SAMBANOVA_BASE_URL", "https://api.sambanova.ai/v1")

class MedicalRAG:
    def __init__(self):
        """Initialize the Medical RAG system"""
        # Validate environment variables
        if not PINECONE_API_KEY:
            raise ValueError("PINECONE_API_KEY not found in environment variables")
        if not LLM_API_KEY:
            raise ValueError("LLM_API_KEY not found in environment variables")
        
        # Initialize Pinecone - Updated for Pinecone SDK v7+
        self.pc = Pinecone(api_key=PINECONE_API_KEY)
        self.index = self.pc.Index("medical-records")
        
        # LLM configuration
        self.llm_model = "Meta-Llama-3.3-70B-Instruct"
        
        # Chat history
        self.chat_history: List[Dict[str, str]] = []
        
        logger.info("Medical RAG system initialized successfully")
    
    def search_similar_documents(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search for similar documents in Pinecone based on the query"""
        try:
            logger.info(f"Searching for similar documents for query: {query[:50]}...")
            # Generate embedding for the query
            query_embedding = self.get_embedding(query)
            
            if query_embedding is None:
                logger.warning("Failed to generate query embedding")
                return []
            
            # Search in Pinecone
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True
            )
            
            # Extract matches from results - correct way for Pinecone client
            matches = []
            # Access matches using getattr to avoid linter issues
            scored_vectors = list(getattr(results, 'matches', []))
            for match in scored_vectors:
                matches.append({
                    'id': getattr(match, 'id', ''),
                    'score': getattr(match, 'score', 0.0),
                    'metadata': dict(getattr(match, 'metadata', {}))
                })
            
            logger.info(f"Found {len(matches)} similar documents")
            return matches
            
        except Exception as error:
            logger.error(f"Error searching documents: {error}")
            return []
    
    def get_embedding(self, text: str) -> Optional[List[float]]:
        """Generate embedding for text using Sambanova API"""
        try:
            headers = {
                "Authorization": f"Bearer {LLM_API_KEY}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "E5-Mistral-7B-Instruct",
                "input": text
            }
            
            logger.debug(f"Generating embedding for text (length: {len(text)} chars)")
            response = requests.post(
                f"{SAMBANOVA_BASE_URL}/embeddings",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and len(data['data']) > 0:
                    logger.debug("Successfully generated embedding")
                    return data['data'][0]['embedding']
                else:
                    logger.error("Unexpected embedding response format")
                    return None
            else:
                logger.error(f"Error generating embedding: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            logger.error("Request timeout while generating embedding")
            return None
        except Exception as error:
            logger.error(f"Error generating embedding: {error}")
            return None
    
    def format_context(self, documents: List[Dict]) -> str:
        """Format retrieved documents as context for the LLM"""
        if not documents:
            logger.warning("No documents to format as context")
            return "No relevant documents found."
        
        context = ""
        for i, doc in enumerate(documents):
            metadata = doc.get('metadata', {})
            score = doc.get('score', 0.0)
            
            context += f"Document {i+1}:\n"
            context += f"Content: {metadata.get('content', 'N/A')}\n"
            context += f"Source: {metadata.get('source', 'N/A')}\n"
            context += f"Relevance Score: {score:.4f}\n\n"
        return context
    
    def generate_response(self, query: str, context_documents: List[Dict]) -> str:
        """Generate response using the LLM with RAG context"""
        try:
            # Format context from retrieved documents
            context = self.format_context(context_documents)
            logger.info(f"Formatted context with {len(context_documents)} documents")
            
            # Prepare chat history (last 3 turns for context)
            chat_history = ""
            if self.chat_history:
                for turn in self.chat_history[-3:]:
                    chat_history += f"Human: {turn['query']}\nAssistant: {turn['response']}\n\n"
            
            # Create prompt with RAG context
            if chat_history:
                chat_history_text = f"Conversation History:\n{chat_history}"
            else:
                chat_history_text = ""
            
            prompt = f"""You are a medical assistant AI. Use the following medical records and conversation history to answer the user's question.

{chat_history_text}

Relevant Medical Records:
{context}

User Question: {query}

Instructions:
1. If the question asks for diagnostic differentials or possible diagnoses, provide a numbered list of potential diagnoses based on the patient's symptoms and medical history from the records.
2. Base your diagnostic differentials ONLY on the specific patient information provided in the records above.
3. If the question is about a specific patient, only answer based on the records provided.
4. Keep responses concise and under 30 seconds of reading time.
5. If you don't have enough information, please say so.
6. Focus on medical facts from the provided records rather than general medical knowledge.
7. Address the user as a medical professional (doctor).
8. Be direct and avoid unnecessary explanations."""

            # Call LLM API
            headers = {
                "Authorization": f"Bearer {LLM_API_KEY}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.llm_model,
                "messages": [
                    {"role": "system", "content": "You are a medical assistant AI specialized in analyzing patient records and providing diagnostic differentials when requested. Always base your responses on the specific patient information provided in the records. Address the user as a medical professional (doctor). Be direct and concise."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 300  # Further reduced for more concise responses
            }
            
            logger.info("Generating response with LLM...")
            response = requests.post(
                f"{SAMBANOVA_BASE_URL}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'choices' in data and len(data['choices']) > 0:
                    logger.info("Successfully generated response")
                    return data['choices'][0]['message']['content']
                else:
                    logger.error("Unexpected response format from LLM")
                    return "Sorry, I received an unexpected response format."
            else:
                logger.error(f"Error generating response: {response.status_code} - {response.text}")
                return "Sorry, I encountered an error while generating the response."
                
        except requests.exceptions.Timeout:
            logger.error("Request timeout while generating response")
            return "Sorry, the request timed out. Please try again."
        except Exception as error:
            logger.error(f"Error generating response: {error}")
            return "Sorry, I encountered an error while generating the response."
    
    def ask_question(self, query: str) -> str:
        """Main method to ask a question and get a response"""
        if not query or not query.strip():
            logger.warning("Empty or invalid question provided")
            return "Please provide a valid question."
        
        logger.info(f"Processing question: {query[:50]}...")
        # Search for relevant documents
        relevant_docs = self.search_similar_documents(query)
        
        if not relevant_docs:
            response = "I couldn't find any relevant medical records to answer your question."
        else:
            # Generate response using LLM with RAG
            response = self.generate_response(query, relevant_docs)
        
        # Store in chat history
        self.chat_history.append({
            "query": query,
            "response": response
        })
        
        # Keep only last 10 turns
        if len(self.chat_history) > 10:
            self.chat_history.pop(0)
        
        logger.info("Question processed successfully")
        return response

def main():
    """Main function to demonstrate the Medical RAG system"""
    try:
        logger.info("Initializing Medical RAG System...")
        rag = MedicalRAG()
        
        logger.info("Medical RAG System is ready!")
        print("You can ask questions about medical records. Type 'quit' to exit.")
        print("-" * 50)
        
        while True:
            try:
                query = input("\nYour question: ").strip()
                
                if query.lower() in ['quit', 'exit', 'q']:
                    logger.info("User requested to quit")
                    print("Thank you for using the Medical RAG System!")
                    break
                
                if query:
                    response = rag.ask_question(query)
                    print(f"\nAssistant: {response}")
                else:
                    print("Please enter a valid question.")
                    
            except KeyboardInterrupt:
                logger.info("User interrupted the program")
                print("\n\nThank you for using the Medical RAG System!")
                break
            except Exception as error:
                logger.error(f"An error occurred: {error}")
                print(f"An error occurred: {error}")
                
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        print(f"Configuration error: {e}")
        print("Please check your .env file and ensure all required API keys are set.")
    except Exception as e:
        logger.error(f"Failed to initialize Medical RAG System: {e}")
        print(f"Failed to initialize Medical RAG System: {e}")

if __name__ == "__main__":
    # Set up logging for standalone execution
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    main()