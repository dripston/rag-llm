"""
Script to add new data directly to Pinecone without reprocessing all existing data
"""

import os
import json
from dotenv import load_dotenv
from pinecone import Pinecone
import asyncio
from chunk_prisma_data import convert_to_documents
from generate_embeddings import get_embedding_with_fallback

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

async def add_new_data_to_pinecone():
    """Add new data directly to Pinecone"""
    try:
        # New data to add
        new_data = {
            "hospitals": [
                {
                    "hospital_id": "HOSP004",
                    "hospital_name": "Metropolitan Medical Center",
                    "address": "789 Healthcare Drive, MetroCity",
                    "phone_number": "+1-555-0199",
                    "created_at": "2025-11-13 19:13:04.588000"
                }
            ],
            "doctors": [
                {
                    "doctor_id": "DOC006",
                    "doctor_name": "Dr. James Wilson",
                    "hospital_id": "HOSP004",
                    "phone_number": "+1-555-0198",
                    "certificate_url": "https://example.com/certificates/jwilson.pdf",
                    "id_document_url": "https://example.com/ids/jwilson.pdf",
                    "profile_image_url": "https://example.com/profiles/jwilson.jpg",
                    "created_at": "2025-11-13 19:13:04.588000"
                }
            ],
            "users": [
                {
                    "user_id": "USR006",
                    "user_name": "Olivia Brown",
                    "user_mobile": "+1-555-0197",
                    "address": "321 Wellness Street, HealthVille",
                    "treated_by": "DOC006",
                    "hospital_id": "HOSP004",
                    "transcripted_data": "Patient reports seasonal allergies and mild asthma",
                    "audio_url": "https://example.com/audio/olivia_brown_20231016.wav",
                    "created_at": "2025-11-13 19:13:04.588000"
                }
            ]
        }
        
        print("Converting new data to documents...")
        documents = convert_to_documents(new_data)
        print(f"Generated {len(documents)} documents")
        
        # Initialize Pinecone
        print("Initializing Pinecone...")
        pc = Pinecone(api_key=PINECONE_API_KEY)
        index = pc.Index("medical-records")
        
        # Get current vector count to determine new IDs
        stats = index.describe_index_stats()
        current_vector_count = stats.total_vector_count
        print(f"Current vector count: {current_vector_count}")
        
        # Generate embeddings for new documents
        print("Generating embeddings for new documents...")
        vectors = []
        for i, doc in enumerate(documents):
            print(f"Generating embedding for document {i+1}/{len(documents)}...")
            
            # Get embedding for the document content
            embedding = get_embedding_with_fallback(doc.page_content)
            
            if embedding is not None:
                # Create a unique ID for each vector
                vector_id = f"chunk_{current_vector_count + i}"
                
                # Prepare metadata
                metadata = doc.metadata.copy()
                metadata["content"] = doc.page_content
                
                # Clean metadata
                cleaned_metadata = clean_metadata(metadata)
                
                # Create vector record
                vector_record = {
                    "id": vector_id,
                    "values": embedding,
                    "metadata": cleaned_metadata
                }
                
                vectors.append(vector_record)
                print(f"  ✓ Embedding generated (dimension: {len(embedding)})")
            else:
                print(f"  ✗ Failed to generate embedding for document {i+1}")
        
        # Store new vectors in Pinecone
        if vectors:
            print(f"Upserting {len(vectors)} new vectors to Pinecone...")
            index.upsert(vectors=vectors)
            print(f"Successfully added {len(vectors)} new vectors to Pinecone!")
            return True
        else:
            print("No vectors to upsert")
            return False
            
    except Exception as e:
        print(f"Error adding new data to Pinecone: {e}")
        return False

if __name__ == "__main__":
    print("Adding new data to Pinecone...")
    result = asyncio.run(add_new_data_to_pinecone())
    if result:
        print("✓ Successfully added new data to Pinecone")
    else:
        print("✗ Failed to add new data to Pinecone")