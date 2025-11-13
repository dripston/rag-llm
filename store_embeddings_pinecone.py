import os
import json
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
import time

# Load environment variables
load_dotenv()

# Pinecone configuration
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

def clean_metadata(metadata):
    """Clean metadata to remove null values and ensure all values are valid for Pinecone"""
    cleaned = {}
    for key, value in metadata.items():
        # Skip null/None values
        if value is not None:
            # Convert value to string if it's not already a string, number, or boolean
            if isinstance(value, (str, int, float, bool)):
                cleaned[key] = value
            else:
                cleaned[key] = str(value)
    return cleaned

def initialize_pinecone():
    """Initialize Pinecone client and create index if it doesn't exist"""
    try:
        # Initialize Pinecone client
        pc = Pinecone(api_key=PINECONE_API_KEY)
        
        # Define index name
        index_name = "medical-records"
        
        # Check if index exists
        existing_indexes = pc.list_indexes()
        
        if index_name not in [idx['name'] for idx in existing_indexes]:
            print(f"Creating Pinecone index: {index_name}")
            # Create index
            pc.create_index(
                name=index_name,
                dimension=4096,  # E5-Mistral-7B-Instruct embedding dimension
                metric="cosine",  # Cosine similarity
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )
            # Wait for index to be ready
            time.sleep(10)
            print(f"Index {index_name} created successfully")
        else:
            print(f"Index {index_name} already exists")
        
        # Connect to the index
        index = pc.Index(index_name)
        return index
        
    except Exception as error:
        print(f"Error initializing Pinecone: {error}")
        return None

def store_embeddings_in_pinecone():
    """Store embeddings in Pinecone database"""
    try:
        # Initialize Pinecone
        index = initialize_pinecone()
        if not index:
            print("Failed to initialize Pinecone")
            return False
        
        # Load embedded data
        print("Loading embedded data...")
        with open("embedded_prisma_data.json", "r", encoding="utf-8") as f:
            embedded_data = json.load(f)
        
        print(f"Found {len(embedded_data)} embeddings to store")
        
        # Prepare vectors for upsert
        vectors = []
        for i, item in enumerate(embedded_data):
            # Create a unique ID for each vector
            vector_id = f"chunk_{i}"
            
            # Extract content and metadata
            content = item["content"]
            metadata = item["metadata"]
            
            # Add content to metadata for retrieval
            metadata["content"] = content
            
            # Clean metadata to remove null values
            cleaned_metadata = clean_metadata(metadata)
            
            # Create vector record
            vector_record = {
                "id": vector_id,
                "values": item["embedding"],
                "metadata": cleaned_metadata
            }
            
            vectors.append(vector_record)
            
            # Upsert in batches of 100 (Pinecone's recommended batch size)
            if len(vectors) >= 100 or i == len(embedded_data) - 1:
                print(f"Upserting batch of {len(vectors)} vectors...")
                index.upsert(vectors=vectors)
                print(f"Successfully upserted batch of {len(vectors)} vectors")
                vectors = []  # Reset for next batch
        
        print("All embeddings stored in Pinecone successfully!")
        return True
        
    except Exception as error:
        print(f"Error storing embeddings in Pinecone: {error}")
        return False

if __name__ == "__main__":
    print("Storing embeddings in Pinecone...")
    success = store_embeddings_in_pinecone()
    
    if success:
        print("Embeddings stored successfully!")
    else:
        print("Failed to store embeddings.")