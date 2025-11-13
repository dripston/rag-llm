"""
Script to check if data is properly stored in Pinecone
"""

import os
from dotenv import load_dotenv
from pinecone import Pinecone

# Load environment variables
load_dotenv()

# Configuration
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

def check_pinecone_data():
    """Check if data is properly stored in Pinecone"""
    try:
        if not PINECONE_API_KEY:
            print("Error: PINECONE_API_KEY not found in environment variables")
            return False
            
        # Initialize Pinecone
        pc = Pinecone(api_key=PINECONE_API_KEY)
        index = pc.Index("medical-records")
        
        # Check index stats
        stats = index.describe_index_stats()
        print("Index stats:")
        print(f"  Namespaces: {stats.namespaces}")
        print(f"  Dimension: {stats.dimension}")
        print(f"  Index fullness: {stats.index_fullness}")
        print(f"  Total vector count: {stats.total_vector_count}")
        
        # Try a simple search for HOSP004
        print("\nSearching for HOSP004...")
        results = index.query(
            vector=[0.0] * stats.dimension,  # Zero vector for random search
            top_k=10,
            include_metadata=True
        )
        
        print(f"Found {len(results.matches)} matches")
        hosp004_found = False
        for i, match in enumerate(results.matches):
            metadata = match.metadata if match.metadata else {}
            content = metadata.get('content', '')
            if 'HOSP004' in content:
                print(f"Found HOSP004 in match {i+1}")
                print(f"  ID: {match.id}")
                print(f"  Score: {match.score}")
                print(f"  Content preview: {content[:200]}...")
                hosp004_found = True
        
        if not hosp004_found:
            print("HOSP004 not found in the first 10 search results")
            
        return True
        
    except Exception as e:
        print(f"Error checking Pinecone data: {e}")
        return False

if __name__ == "__main__":
    print("Checking Pinecone data...")
    check_pinecone_data()