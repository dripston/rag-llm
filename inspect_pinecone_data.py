from dotenv import load_dotenv
import os
from pinecone import Pinecone

# Load environment variables
load_dotenv()

# Configuration
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index("medical-records")

# Fetch a few sample records to understand the data structure
results = index.fetch(ids=['chunk_1', 'chunk_2', 'chunk_3'])

print("Sample records from Pinecone:")
for id, record in results['vectors'].items():
    print(f"\nID: {id}")
    if 'metadata' in record:
        metadata = record['metadata']
        print(f"Metadata keys: {list(metadata.keys())}")
        for key, value in metadata.items():
            print(f"  {key}: {str(value)[:100]}{'...' if len(str(value)) > 100 else ''}")
    else:
        print("  No metadata found")