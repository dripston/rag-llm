"""
Test script to verify that logging is working correctly across all modules
"""

import logging
import asyncio
from chunk_prisma_data import fetch_prisma_data
from generate_embeddings import get_embedding_with_fallback
from store_embeddings_pinecone import store_embeddings_in_pinecone
from medical_rag import MedicalRAG

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

async def test_logging():
    """Test logging across all modules"""
    logger.info("Starting logging test...")
    
    # Test chunk_prisma_data logging
    logger.info("Testing chunk_prisma_data module...")
    try:
        data = await fetch_prisma_data()
        logger.info(f"Successfully fetched {len(data)} tables from database")
    except Exception as e:
        logger.error(f"Error in chunk_prisma_data: {e}")
    
    # Test generate_embeddings logging
    logger.info("Testing generate_embeddings module...")
    try:
        test_text = "This is a test text for embedding generation"
        embedding = get_embedding_with_fallback(test_text)
        if embedding:
            logger.info(f"Successfully generated embedding with {len(embedding)} dimensions")
        else:
            logger.warning("Failed to generate embedding")
    except Exception as e:
        logger.error(f"Error in generate_embeddings: {e}")
    
    # Test store_embeddings_pinecone logging
    logger.info("Testing store_embeddings_pinecone module...")
    try:
        success = store_embeddings_in_pinecone()
        if success:
            logger.info("Successfully stored embeddings in Pinecone")
        else:
            logger.warning("Failed to store embeddings in Pinecone")
    except Exception as e:
        logger.error(f"Error in store_embeddings_pinecone: {e}")
    
    # Test medical_rag logging
    logger.info("Testing medical_rag module...")
    try:
        rag = MedicalRAG()
        logger.info("Successfully initialized MedicalRAG")
    except Exception as e:
        logger.error(f"Error in medical_rag: {e}")
    
    logger.info("Logging test completed!")

if __name__ == "__main__":
    asyncio.run(test_logging())