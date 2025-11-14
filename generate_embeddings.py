import os
import json
import requests
import time
import logging
from dotenv import load_dotenv

# Set up logging
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configuration
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
LLM_API_KEY = os.getenv("LLM_API_KEY")
SAMBANOVA_BASE_URL = os.getenv("SAMBANOVA_BASE_URL", "https://api.sambanova.ai/v1")

# Fallback API keys (if available)
FALLBACK_API_KEYS = [
    os.getenv("FALLBACK_API_KEY_1"),
    os.getenv("FALLBACK_API_KEY_2"),
    os.getenv("FALLBACK_API_KEY_3"),
    os.getenv("FALLBACK_API_KEY_4"),
    os.getenv("FALLBACK_API_KEY_5")
]

def get_sambanova_embedding(text, api_key=None):
    """Generate embedding for text using Sambanova API"""
    current_api_key = None
    try:
        # Use provided API key or default
        current_api_key = api_key or LLM_API_KEY
        
        if not current_api_key:
            logger.error("No API key available for Sambanova")
            return None
            
        headers = {
            "Authorization": f"Bearer {current_api_key}",
            "Content-Type": "application/json"
        }
        
        # Use the correct model name
        payload = {
            "model": "E5-Mistral-7B-Instruct",
            "input": text
        }
        
        # Try the standard embeddings endpoint
        url = f"{SAMBANOVA_BASE_URL}/embeddings"
        
        logger.debug(f"Generating embedding for text (length: {len(text)} chars)")
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            logger.debug("Successfully generated embedding")
            return data['data'][0]['embedding']
        elif response.status_code == 429:
            # Rate limit hit
            key_display = "Unknown"
            if current_api_key:
                key_str = str(current_api_key)
                key_display = key_str[:8] if len(key_str) > 8 else key_str
            logger.warning(f"Rate limit hit with API key: {key_display}...")
            return None
        else:
            key_display = "Unknown"
            if current_api_key:
                key_str = str(current_api_key)
                key_display = key_str[:8] if len(key_str) > 8 else key_str
            logger.error(f"Error with API key {key_display}...: {response.status_code} - {response.text}")
            return None
            
    except Exception as error:
        key_display = "Unknown"
        if current_api_key:
            key_str = str(current_api_key)
            key_display = key_str[:8] if len(key_str) > 8 else key_str
        logger.error(f"Error generating embedding with API key {key_display}...: {error}")
        return None

def get_embedding_with_fallback(text):
    """Try to get embedding using primary key, then fallback keys"""
    # Try primary API key first
    logger.debug("Trying primary API key...")
    embedding = get_sambanova_embedding(text)
    if embedding is not None:
        logger.debug("Successfully generated embedding with primary API key")
        return embedding
    
    # Log available fallback keys for debugging
    available_keys = [key for key in FALLBACK_API_KEYS if key]
    logger.info(f"Primary key failed, trying {len(available_keys)} fallback keys...")
    
    # Try fallback API keys
    for i, fallback_key in enumerate(FALLBACK_API_KEYS):
        if fallback_key:
            logger.info(f"Trying fallback API key {i+1}...")
            embedding = get_sambanova_embedding(text, fallback_key)
            if embedding is not None:
                logger.info(f"  ✓ Success with fallback API key {i+1}")
                return embedding
            time.sleep(1)  # Small delay between attempts
    
    logger.error("Failed to generate embedding with all available API keys")
    return None

def load_existing_embeddings():
    """Load existing embeddings if they exist and are valid"""
    try:
        if os.path.exists("embedded_prisma_data.json"):
            with open("embedded_prisma_data.json", "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:  # Check if file is not empty
                    data = json.loads(content)
                    if isinstance(data, list):  # Check if it's a list
                        logger.info(f"Loaded {len(data)} existing embeddings")
                        return data
                    else:
                        logger.warning("Existing embeddings file has invalid format")
                        return []
                else:
                    logger.warning("Existing embeddings file is empty")
                    return []
        return []
    except json.JSONDecodeError as json_error:
        logger.error(f"Error parsing existing embeddings JSON: {json_error}")
        # Try to salvage what we can or start fresh
        return []
    except Exception as error:
        logger.error(f"Error loading existing embeddings: {error}")
        return []

def generate_embeddings_for_chunks():
    """Generate embeddings for all chunked data"""
    try:
        # Load chunked data
        logger.info("Loading chunked data...")
        with open("chunked_prisma_data.json", "r", encoding="utf-8") as f:
            chunks = json.load(f)
        
        # Load existing embeddings
        existing_embeddings = load_existing_embeddings()
        
        logger.info(f"Found {len(chunks)} chunks to process")
        logger.info(f"Already processed: {len(existing_embeddings)} chunks")
        
        # Create a set of already processed chunk contents for quick lookup
        processed_contents = {embedding.get('content', '') for embedding in existing_embeddings}
        
        # Filter out already processed chunks
        new_chunks = [chunk for chunk in chunks if chunk['content'] not in processed_contents]
        
        logger.info(f"New chunks to process: {len(new_chunks)}")
        
        # If no new chunks, we're done
        if not new_chunks:
            logger.info("No new chunks to process!")
            return existing_embeddings
        
        # Process new chunks
        logger.info(f"Processing {len(new_chunks)} new chunks...")
        for i, chunk in enumerate(new_chunks):
            logger.info(f"Generating embedding for new chunk {i+1}/{len(new_chunks)}...")
            
            # Add small delay to avoid rate limits
            time.sleep(0.5)
            
            # Get embedding for the chunk content using fallback mechanism
            embedding = get_embedding_with_fallback(chunk['content'])
            
            if embedding is not None:
                # Add embedding to chunk data
                embedded_chunk = {
                    "content": chunk['content'],
                    "metadata": chunk['metadata'],
                    "embedding": embedding
                }
                existing_embeddings.append(embedded_chunk)
                logger.info(f"  ✓ Embedding generated (dimension: {len(embedding)})")
                
                # Save progress after each successful embedding
                with open("embedded_prisma_data.json", "w", encoding="utf-8") as f:
                    json.dump(existing_embeddings, f, indent=2)
            else:
                logger.error(f"  ✗ Failed to generate embedding for chunk {i+1}")
        
        logger.info(f"Successfully generated embeddings for {len(existing_embeddings)} chunks")
        logger.info("Embedded data saved to 'embedded_prisma_data.json'")
        
        return existing_embeddings
        
    except Exception as error:
        logger.error(f"Error generating embeddings: {error}")
        return []

if __name__ == "__main__":
    # Set up logging for standalone execution
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    logger.info("Generating embeddings for chunked medical data...")
    logger.info(f"Using Sambanova API: {SAMBANOVA_BASE_URL}")
    logger.info(f"Model: E5-Mistral-7B-Instruct")
    
    embedded_chunks = generate_embeddings_for_chunks()
    
    if embedded_chunks:
        logger.info("Embedding generation completed successfully!")
    else:
        logger.error("Failed to generate embeddings.")