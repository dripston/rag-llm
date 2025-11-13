import requests
import json

# Test the API endpoints
BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print("Health Check:")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        print()
    except Exception as e:
        print(f"Health check failed: {e}")
        print()

def test_ask():
    """Test the ask endpoint"""
    try:
        data = {"question": "What are the diagnostic differentials for chest pain?"}
        response = requests.post(f"{BASE_URL}/ask", json=data)
        print("Ask Endpoint:")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Question: {result.get('question')}")
            print(f"Answer: {result.get('answer')[:200]}...")
        else:
            print(f"Error: {response.text}")
        print()
    except Exception as e:
        print(f"Ask endpoint test failed: {e}")
        print()

def test_update_rag():
    """Test the update RAG endpoint"""
    try:
        data = {"patient_id": "USR003", "new_data": "Patient reported increased chest pain"}
        response = requests.post(f"{BASE_URL}/update_rag", json=data)
        print("Update RAG Endpoint:")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Response: {result}")
        else:
            print(f"Error: {response.text}")
        print()
    except Exception as e:
        print(f"Update RAG endpoint test failed: {e}")
        print()

if __name__ == "__main__":
    print("Testing Medical RAG API endpoints...")
    print("=" * 50)
    test_health()
    test_ask()
    test_update_rag()