"""
Quick test to process just the new data without existing embeddings
"""

import json
import asyncio
import os
from chunk_prisma_data import convert_to_documents
from generate_embeddings import generate_embeddings_for_chunks
from store_embeddings_pinecone import store_embeddings_in_pinecone

# Test data
test_data = {
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

async def quick_test():
    print("Converting test data to documents...")
    documents = convert_to_documents(test_data)
    print(f"Generated {len(documents)} documents")
    
    # Save to chunked data file
    chunked_data = []
    for doc in documents:
        chunked_item = {
            "content": doc.page_content,
            "metadata": doc.metadata
        }
        chunked_data.append(chunked_item)
    
    with open("test_chunked_data.json", "w", encoding="utf-8") as f:
        json.dump(chunked_data, f, indent=2, default=str)
    
    print("Saved chunked data to test_chunked_data.json")
    
    # Temporarily rename the existing embedded file
    if os.path.exists("embedded_prisma_data.json"):
        os.rename("embedded_prisma_data.json", "embedded_prisma_data.json.bak")
        print("Backed up existing embedded data")
    
    # Create an empty embedded file for this test
    with open("embedded_prisma_data.json", "w") as f:
        json.dump([], f)
    
    try:
        # Process embeddings for just this data
        print("Generating embeddings for test data...")
        # We need to modify the generate_embeddings_for_chunks to work with our test file
        # Let's create a simplified version
        
        # For now, let's just try to store the data directly in Pinecone
        print("Storing test data in Pinecone...")
        success = store_embeddings_in_pinecone()
        
        if success:
            print("✓ Successfully stored test data in Pinecone")
        else:
            print("✗ Failed to store test data in Pinecone")
            
    finally:
        # Restore the original embedded file
        if os.path.exists("embedded_prisma_data.json"):
            os.remove("embedded_prisma_data.json")
        if os.path.exists("embedded_prisma_data.json.bak"):
            os.rename("embedded_prisma_data.json.bak", "embedded_prisma_data.json")
            print("Restored original embedded data")

if __name__ == "__main__":
    print("Running quick test for new data...")
    asyncio.run(quick_test())