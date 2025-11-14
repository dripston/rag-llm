"""
Script to update the RAG system with new data from the Prisma database.
This would typically be run periodically or triggered by new data inserts.
"""

import os
import json
import logging
from dotenv import load_dotenv
from chunk_prisma_data import fetch_prisma_data, convert_to_documents
from generate_embeddings import generate_embeddings_for_chunks
from store_embeddings_pinecone import store_embeddings_in_pinecone
import asyncio
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

async def update_rag_with_new_data():
    """Update the RAG system with new data from Prisma database"""
    try:
        logger.info("Fetching new data from Prisma database...")
        data = await fetch_prisma_data()
        
        if not data:
            logger.warning("No data fetched from database")
            return False
            
        return await process_rag_update(data)
        
    except Exception as e:
        logger.error(f"Error updating RAG: {e}")
        return False

async def update_rag_with_provided_data(data):
    """Update the RAG system with provided data"""
    try:
        if not data:
            logger.warning("No data provided for RAG update")
            return False
            
        return await process_rag_update(data)
        
    except Exception as e:
        logger.error(f"Error updating RAG with provided data: {e}")
        return False

async def process_rag_update(data):
    """Process RAG update with provided data"""
    try:
        logger.info("Converting data to documents...")
        documents = convert_to_documents(data)
        
        if not documents:
            logger.warning("No documents generated from data")
            return False
            
        logger.info(f"Generated {len(documents)} documents")
        
        # Load existing chunked data if it exists
        existing_chunked_data = []
        if os.path.exists("chunked_prisma_data.json"):
            try:
                with open("chunked_prisma_data.json", "r", encoding="utf-8") as f:
                    existing_chunked_data = json.load(f)
                logger.info(f"Loaded {len(existing_chunked_data)} existing chunks")
            except Exception as e:
                logger.warning(f"Could not load existing chunked data: {e}")
                existing_chunked_data = []
        
        # Convert new documents to chunked format
        new_chunked_data = []
        for i, doc in enumerate(documents):
            chunked_item = {
                "content": doc.page_content,
                "metadata": doc.metadata
            }
            new_chunked_data.append(chunked_item)
        
        # Combine existing and new data
        combined_chunked_data = existing_chunked_data + new_chunked_data
        
        # Save combined documents to chunked_prisma_data.json for processing
        with open("chunked_prisma_data.json", "w", encoding="utf-8") as f:
            json.dump(combined_chunked_data, f, indent=2, default=str)
        
        logger.info(f"Total chunks to process: {len(combined_chunked_data)} ({len(existing_chunked_data)} existing, {len(new_chunked_data)} new)")
        
        logger.info("Generating embeddings...")
        embeddings_data = generate_embeddings_for_chunks()
        
        logger.info("Storing embeddings in Pinecone...")
        success = store_embeddings_in_pinecone()
        
        if success:
            logger.info("RAG update completed successfully!")
        else:
            logger.error("Failed to update RAG system")
            
        return success
        
    except Exception as e:
        logger.error(f"Error processing RAG update: {e}")
        return False

async def update_rag_from_file(file_path):
    """Update RAG system from a JSON file containing data"""
    try:
        logger.info(f"Loading data from {file_path}...")
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        result = await process_rag_update(data)
        
        if result:
            logger.info(f"Successfully processed RAG update from {file_path}")
        else:
            logger.error(f"Failed to process RAG update from {file_path}")
            
        return result
        
    except Exception as e:
        logger.error(f"Error updating RAG from file: {e}")
        return False

if __name__ == "__main__":
    logger.info("Starting RAG update process...")
    result = asyncio.run(update_rag_with_new_data())
    if result:
        logger.info("RAG update completed successfully!")
    else:
        logger.error("RAG update failed!")