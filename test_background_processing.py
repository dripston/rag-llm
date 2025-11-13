"""
Test script to simulate background processing of RAG updates
"""

import json
import asyncio
from update_rag import update_rag_from_file

# Create a test file with the data we want to process
# This should be in the format expected by convert_to_documents
test_file_data = {
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

# For the update_rag_from_file function, we need to convert this to the chunked format
# Let's create a separate test for the process_rag_update function directly
from update_rag import process_rag_update

print("Testing process_rag_update function directly...")
try:
    result = asyncio.run(process_rag_update(test_file_data))
    if result:
        print("✓ Successfully processed test data")
    else:
        print("✗ Failed to process test data")
except Exception as e:
    print(f"Error processing test data: {e}")