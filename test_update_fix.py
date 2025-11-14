import json
import os
from chunk_prisma_data import convert_to_documents

def test_update_fix():
    """Test the update fix with USR099 data"""
    
    # Load existing chunked data
    existing_chunked_data = []
    if os.path.exists("chunked_prisma_data.json"):
        try:
            with open("chunked_prisma_data.json", "r", encoding="utf-8") as f:
                existing_chunked_data = json.load(f)
            print(f"Loaded {len(existing_chunked_data)} existing chunks")
        except Exception as e:
            print(f"Could not load existing chunked data: {e}")
            existing_chunked_data = []
    
    # USR099 data
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
    
    # Convert new documents to chunked format
    documents = convert_to_documents(data)
    print(f"Generated {len(documents)} new documents")
    
    new_chunked_data = []
    for i, doc in enumerate(documents):
        chunked_item = {
            "content": doc.page_content,
            "metadata": doc.metadata
        }
        new_chunked_data.append(chunked_item)
    
    # Combine existing and new data, removing duplicates based on content
    # Use a more robust deduplication approach
    combined_chunked_data = existing_chunked_data.copy()
    existing_content_set = set()
    
    # Add existing content to the set for deduplication
    for chunk in existing_chunked_data:
        content = chunk.get('content', '')
        # Use a normalized version of the content for comparison
        normalized_content = ' '.join(content.split())
        existing_content_set.add(normalized_content)
    
    # Add new chunks that don't already exist
    added_count = 0
    for new_chunk in new_chunked_data:
        content = new_chunk.get('content', '')
        # Use a normalized version of the content for comparison
        normalized_content = ' '.join(content.split())
        
        if normalized_content not in existing_content_set:
            combined_chunked_data.append(new_chunk)
            existing_content_set.add(normalized_content)
            added_count += 1
            print(f"Added new chunk: {content[:50]}...")
        else:
            print("Chunk already exists, skipping")
    
    print(f"Total chunks: {len(combined_chunked_data)} ({len(existing_chunked_data)} existing, {added_count} added)")
    
    # Save the result
    with open("chunked_prisma_data.json", "w", encoding="utf-8") as f:
        json.dump(combined_chunked_data, f, indent=2, default=str)
    
    print("Updated chunked_prisma_data.json")

if __name__ == "__main__":
    test_update_fix()