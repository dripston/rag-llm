import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_api_key(api_key, base_url="https://api.sambanova.ai/v1"):
    """Test if an API key works and is not returning 429 errors"""
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Simple test text
    test_text = "This is a test sentence for embedding generation."
    
    payload = {
        "model": "E5-Mistral-7B-Instruct",
        "input": test_text
    }
    
    try:
        print(f"Testing API key: {api_key[:8]}...")
        response = requests.post(
            f"{base_url}/embeddings",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            embedding = data['data'][0]['embedding']
            print(f"✓ SUCCESS: API key is working")
            print(f"  - Status code: {response.status_code}")
            print(f"  - Embedding dimension: {len(embedding)}")
            return True
        elif response.status_code == 429:
            print(f"✗ RATE LIMIT: API key is rate limited (429)")
            print(f"  - Response: {response.text}")
            return False
        else:
            print(f"✗ ERROR: API key failed with status {response.status_code}")
            print(f"  - Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ EXCEPTION: Failed to test API key: {e}")
        return False

if __name__ == "__main__":
    # Test the key provided by user
    test_key = "843b9ffd-1e8d-4ee2-8ff1-4abf1fb3d770"
    print("Testing user-provided API key:")
    test_api_key(test_key)
    
    print("\n" + "="*50)
    
    # Test primary API key from environment
    primary_key = os.getenv("LLM_API_KEY")
    if primary_key:
        print("Testing primary API key from environment:")
        test_api_key(primary_key)
    
    print("\n" + "="*50)
    
    # Test fallback API keys from environment
    for i in range(1, 6):
        fallback_key_var = f"FALLBACK_API_KEY_{i}"
        fallback_key = os.getenv(fallback_key_var)
        if fallback_key:
            print(f"Testing {fallback_key_var}:")
            test_api_key(fallback_key)