import json
from chunk_prisma_data import convert_to_documents

def test_data_processing():
    """Test data processing with USR099 data"""
    
    # This is the data structure you're sending
    data = {
        "users": [
            {
                "user_id": "USR099",
                "user_name": "Rahul Verma",
                "user_mobile": "9123456780",
                "address": "12 Lotus Residency, Mumbai",
                "treated_by": "DR009",
                "hospital_id": "HOSP004",
                "transcripted_data": "Patient has mild throat pain and cough",
                "audio_url": "https://example.com/audio/99",
                "created_at": "2025-11-14T12:00:00Z"
            }
        ]
    }
    
    print("Converting data to documents...")
    documents = convert_to_documents(data)
    print(f"Generated {len(documents)} documents")
    
    for i, doc in enumerate(documents):
        print(f"\nDocument {i+1}:")
        print(f"Content: {doc.page_content}")
        print(f"Metadata: {doc.metadata}")

if __name__ == "__main__":
    test_data_processing()