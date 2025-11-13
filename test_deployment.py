"""
Script to test the deployment of the Medical RAG API
"""

import requests
import time
import json

def test_api_deployment():
    """Test the API deployment"""
    print("Testing Medical RAG API deployment...")
    print("=" * 50)
    
    # Test health endpoint
    try:
        print("1. Testing health endpoint...")
        response = requests.get("http://localhost:8000/health")
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Response: {data}")
        else:
            print(f"   Error: {response.text}")
        print()
    except Exception as e:
        print(f"   Health check failed: {e}")
        print()
    
    # Test ask endpoint
    try:
        print("2. Testing ask endpoint...")
        question_data = {"question": "What are the diagnostic differentials for chest pain?"}
        response = requests.post("http://localhost:8000/ask", json=question_data)
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Question: {data.get('question')}")
            print(f"   Answer: {data.get('answer')[:100]}...")
        else:
            print(f"   Error: {response.text}")
        print()
    except Exception as e:
        print(f"   Ask endpoint test failed: {e}")
        print()
    
    # Test update RAG endpoint
    try:
        print("3. Testing update RAG endpoint...")
        update_data = {"patient_id": "USR003", "new_data": "Patient reported increased chest pain"}
        response = requests.post("http://localhost:8000/update_rag", json=update_data)
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Response: {data}")
        else:
            print(f"   Error: {response.text}")
        print()
    except Exception as e:
        print(f"   Update RAG endpoint test failed: {e}")
        print()

if __name__ == "__main__":
    test_api_deployment()