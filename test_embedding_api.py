"""
Test script to check if the embedding API is working
"""

import os
from dotenv import load_dotenv
from generate_embeddings import get_embedding_with_fallback

# Load environment variables
load_dotenv()

def test_embedding():
    """Test the embedding API with a simple text"""
    test_text = "Hospital Information: Metropolitan Medical Center"
    
    print("Testing embedding generation...")
    print(f"Test text: {test_text}")
    
    embedding = get_embedding_with_fallback(test_text)
    
    if embedding is not None:
        print(f"✓ Successfully generated embedding (dimension: {len(embedding)})")
        return True
    else:
        print("✗ Failed to generate embedding")
        return False

if __name__ == "__main__":
    test_embedding()