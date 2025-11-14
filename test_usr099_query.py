import os
import json
from dotenv import load_dotenv
from pinecone import Pinecone

# Load environment variables
load_dotenv()

def test_usr099_query():
    """Test querying for USR099 specifically"""
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
        
        # Try querying for "USR099" specifically
        print("\nQuerying for 'USR099'...")
        
        # We need to generate an embedding for "USR099"
        # But for now, let's just do a broad search and filter results
        query_vector = [0.0] * stats.dimension
        
        results = index.query(
            vector=query_vector,
            top_k=20,  # Get more results to increase chances of finding USR099
            include_metadata=True
        )
        
        # Check all results for USR099
        matches = getattr(results, 'matches', [])
        usr099_found = False
        
        print(f"Checking {len(matches)} matches for USR099...")
        for i, match in enumerate(matches):
            metadata = getattr(match, 'metadata', {})
            if metadata:
                content = metadata.get('content', '')
                if 'USR099' in content or 'Rahul Verma' in content:
                    print(f"  *** FOUND USR099 in match {i+1}! ***")
                    print(f"  Content preview: {content[:200]}...")
                    usr099_found = True
        
        if not usr099_found:
            print("USR099 data not found in Pinecone")
            
        # Let's also try a different approach - list some sample content
        print("\nSample content from Pinecone (first 5 entries):")
        for i, match in enumerate(matches[:5]):
            metadata = getattr(match, 'metadata', {})
            if metadata:
                content = metadata.get('content', '')
                lines = content.split('\n')
                if lines:
                    print(f"  {i+1}. {lines[1].strip() if len(lines) > 1 else 'N/A'}")
                
    except Exception as e:
        print(f"Error testing USR099 query: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_usr099_query()