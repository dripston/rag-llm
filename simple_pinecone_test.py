import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Pinecone configuration
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

def main():
    print("Testing Pinecone setup...")
    
    # Check if API key is loaded
    if PINECONE_API_KEY:
        print("✓ Pinecone API key loaded")
        print(f"Key preview: {PINECONE_API_KEY[:10]}...")
    else:
        print("✗ Pinecone API key not found")
        return
    
    # Check if embedded data file exists
    if os.path.exists("embedded_prisma_data.json"):
        print("✓ Embedded data file found")
        
        # Load and check embedded data
        with open("embedded_prisma_data.json", "r", encoding="utf-8") as f:
            embedded_data = json.load(f)
        
        print(f"✓ Loaded {len(embedded_data)} embeddings")
        
        # Show details of first embedding
        if embedded_data:
            first_item = embedded_data[0]
            print(f"✓ First embedding dimension: {len(first_item.get('embedding', []))}")
            print(f"✓ First item metadata keys: {list(first_item.get('metadata', {}).keys())}")
    else:
        print("✗ Embedded data file not found")
        return
    
    print("\nReady to store embeddings in Pinecone!")
    print("Next steps:")
    print("1. Install pinecone: pip install pinecone")
    print("2. Run store_embeddings_pinecone.py")

if __name__ == "__main__":
    main()