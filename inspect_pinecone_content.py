import os
import json
from dotenv import load_dotenv
from pinecone import Pinecone

# Load environment variables
load_dotenv()

def inspect_pinecone_content():
    """Inspect the actual content stored in Pinecone"""
    try:
        # Initialize Pinecone
        PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
        pc = Pinecone(api_key=PINECONE_API_KEY)
        
        # Connect to the index
        index = pc.Index("medical-records")
        
        # First, let's check what's in the embedded data file
        print("Checking embedded data file...")
        if os.path.exists("embedded_prisma_data.json"):
            with open("embedded_prisma_data.json", "r", encoding="utf-8") as f:
                embedded_data = json.load(f)
                print(f"Found {len(embedded_data)} embedded items")
                for i, item in enumerate(embedded_data):  # Show all
                    print(f"\n--- Item {i} ---")
                    content = item.get('content', 'N/A')
                    print(f"Content preview: {content[:200]}...")
                    print(f"Metadata: {item.get('metadata', 'N/A')}")
                    
                    # Check if this contains USR099
                    if 'USR099' in content or 'Rahul Verma' in content:
                        print("  *** This item contains USR099 data! ***")
        else:
            print("embedded_prisma_data.json not found")
            
    except Exception as e:
        print(f"Error inspecting Pinecone content: {e}")

if __name__ == "__main__":
    inspect_pinecone_content()