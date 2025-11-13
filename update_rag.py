"""
Script to update the RAG system with new data from the Prisma database.
This would typically be run periodically or triggered by new data inserts.
"""

import os
import json
from dotenv import load_dotenv
from chunk_prisma_data import fetch_prisma_data, convert_to_documents
from generate_embeddings import generate_embeddings_for_chunks
from store_embeddings_pinecone import store_embeddings_in_pinecone
import asyncio
from datetime import datetime

# Load environment variables
load_dotenv()

async def update_rag_with_new_data():
    """Update the RAG system with new data from Prisma database"""
    try:
        print("Fetching new data from Prisma database...")
        data = await fetch_prisma_data()
        
        if not data:
            print("No data fetched from database")
            return False
            
        return await process_rag_update(data)
        
    except Exception as e:
        print(f"Error updating RAG: {e}")
        return False

async def update_rag_with_provided_data(data):
    """Update the RAG system with provided data"""
    try:
        if not data:
            print("No data provided for RAG update")
            return False
            
        return await process_rag_update(data)
        
    except Exception as e:
        print(f"Error updating RAG with provided data: {e}")
        return False

async def process_rag_update(data):
    """Process RAG update with provided data"""
    try:
        print("Converting data to documents...")
        documents = convert_to_documents(data)
        
        if not documents:
            print("No documents generated from data")
            return False
            
        print(f"Generated {len(documents)} documents")
        
        # Save documents to chunked_prisma_data.json for processing
        chunked_data = []
        for i, doc in enumerate(documents):
            chunked_item = {
                "content": doc.page_content,
                "metadata": doc.metadata
            }
            chunked_data.append(chunked_item)
        
        with open("chunked_prisma_data.json", "w", encoding="utf-8") as f:
            json.dump(chunked_data, f, indent=2, default=str)
        
        print("Generating embeddings...")
        embeddings_data = generate_embeddings_for_chunks()
        
        print("Storing embeddings in Pinecone...")
        success = store_embeddings_in_pinecone()
        
        if success:
            print("RAG update completed successfully!")
        else:
            print("Failed to update RAG system")
            
        return success
        
    except Exception as e:
        print(f"Error processing RAG update: {e}")
        return False

async def update_rag_from_file(file_path):
    """Update RAG system from a JSON file containing data"""
    try:
        print(f"Loading data from {file_path}...")
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        return await process_rag_update(data)
        
    except Exception as e:
        print(f"Error updating RAG from file: {e}")
        return False

if __name__ == "__main__":
    import asyncio
    asyncio.run(update_rag_with_new_data())