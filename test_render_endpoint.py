"""
Test script to simulate sending data to the Render endpoint
"""

import requests
import json
from datetime import datetime

# Test data similar to what would be sent from Prisma
test_data = {
    "timestamp": datetime.now().isoformat(),
    "source": "prisma_database",
    "data": {
        "hospitals": [
            {
                "hospital_id": "HOSP004",
                "hospital_name": "Metropolitan Medical Center",
                "address": "789 Healthcare Drive, MetroCity",
                "phone_number": "+1-555-0199",
                "created_at": "2025-11-13T19:13:04.588000"
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
                "created_at": "2025-11-13T19:13:04.588000"
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
                "created_at": "2025-11-13T19:13:04.588000"
            }
        ]
    }
}

# Send to Render endpoint
url = "https://rag-llm-1.onrender.com/update_rag"
headers = {
    "Content-Type": "application/json"
}

print("Sending test data to Render endpoint...")
print(f"URL: {url}")
print(f"Data keys: {test_data['data'].keys()}")

try:
    response = requests.post(url, json=test_data, headers=headers, timeout=30)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error sending data: {e}")