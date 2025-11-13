"""
Script to inspect the actual content stored in Pinecone
"""

import os
from dotenv import load_dotenv
from pinecone import Pinecone

# Load environment variables
load_dotenv()

# Configuration
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

def inspect_pinecone_content():
    """Inspect the actual content stored in Pinecone"""
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
        print(f"  Total vector count: {stats.total_vector_count}")
        
        # Fetch all vectors (or a sample) to inspect content
        print("\nFetching sample vectors to inspect content...")
        results = index.query(
            vector=[0.0] * stats.dimension,  # Zero vector for random search
            top_k=min(20, stats.total_vector_count),  # Get up to 20 or total count
            include_metadata=True
        )
        
        # Access matches correctly
        matches = getattr(results, 'matches', [])
        print(f"Inspecting {len(matches)} vectors:")
        hospitals_found = set()
        for i, match in enumerate(matches):
            metadata = getattr(match, 'metadata', {}) if hasattr(match, 'metadata') else {}
            content = metadata.get('content', '') if metadata else ''
            source = metadata.get('source', 'unknown') if metadata else 'unknown'
            
            # Look for hospital IDs
            if 'Hospital Information:' in content:
                lines = content.split('\n')
                for line in lines:
                    if line.strip().startswith('ID: HOSP'):
                        hospitals_found.add(line.strip())
                        print(f"  Vector {i+1}: {line.strip()} (Source: {source})")
                        break
            
            # Show first few lines of content for context
            content_lines = content.split('\n')
            if content_lines:
                print(f"    Content preview: {content_lines[0][:50] if content_lines else 'Empty'}...")
        
        print(f"\nHospitals found in Pinecone: {sorted(hospitals_found)}")
        
        # Check if HOSP004 is in the hospitals we added
        if 'ID: HOSP004' in hospitals_found:
            print("✓ HOSP004 found in Pinecone!")
        else:
            print("✗ HOSP004 NOT found in Pinecone")
            
        return True
        
    except Exception as e:
        print(f"Error inspecting Pinecone content: {e}")
        return False

if __name__ == "__main__":
    print("Inspecting Pinecone content...")
    inspect_pinecone_content()