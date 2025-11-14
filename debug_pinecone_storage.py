import os
import json
from dotenv import load_dotenv
from pinecone import Pinecone

# Load environment variables
load_dotenv()

def debug_pinecone_storage():
    """Debug what's actually stored in Pinecone"""
    try:
        # Initialize Pinecone
        PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
        pc = Pinecone(api_key=PINECONE_API_KEY)
        
        # Connect to the index
        index = pc.Index("medical-records")
        
        # Check index stats
        print("Checking Pinecone index stats...")
        stats = index.describe_index_stats()
        print(f"Total vector count: {stats.total_vector_count}")
        print(f"Dimension: {stats.dimension}")
        print(f"Namespaces: {stats.namespaces}")
        
        # Try a broad query to see what's in there
        print("\nPerforming a broad query...")
        # Create a simple query vector (all zeros)
        query_vector = [0.0] * stats.dimension
        
        results = index.query(
            vector=query_vector,
            top_k=10,
            include_metadata=True
        )
        
        # Properly access the matches
        matches = getattr(results, 'matches', [])
        print(f"Found {len(matches)} matches")
        for i, match in enumerate(matches):
            print(f"\n--- Match {i+1} ---")
            # Access match attributes properly
            score = getattr(match, 'score', 0.0)
            print(f"Score: {score}")
            
            metadata = getattr(match, 'metadata', {})
            if metadata:
                content = metadata.get('content', 'N/A')
                print(f"Content preview: {content[:300]}...")
                print(f"Metadata keys: {list(metadata.keys())}")
                
                # Check if this contains USR099 or Rahul Verma
                if 'USR099' in content or 'Rahul Verma' in content:
                    print("  *** FOUND USR099 DATA! ***")
            else:
                print("No metadata found")
                
    except Exception as e:
        print(f"Error debugging Pinecone storage: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_pinecone_storage()