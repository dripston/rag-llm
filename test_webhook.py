"""
Test script for the Prisma webhook handler
"""

import os
import json
from dotenv import load_dotenv
from prisma_webhook_handler import trigger_rag_update

# Load environment variables
load_dotenv()

def test_webhook():
    """Test the webhook functionality"""
    print("Testing Prisma webhook handler...")
    
    # This will fetch data from Prisma and send it to the Render endpoint
    result = trigger_rag_update()
    
    if result:
        print("Webhook test completed successfully!")
    else:
        print("Webhook test failed!")
        
def test_direct_api_call():
    """Test direct API call to Render endpoint"""
    import requests
    from datetime import datetime
    
    RENDER_SERVICE_URL = os.getenv("RENDER_SERVICE_URL", "https://rag-llm-1.onrender.com")
    UPDATE_RAG_ENDPOINT = f"{RENDER_SERVICE_URL}/update_rag"
    
    # Sample test data
    test_data = {
        "patient_id": "TEST001",
        "data": "Patient reported new symptoms of chest pain and shortness of breath",
        "timestamp": datetime.now().isoformat()
    }
    
    try:
        headers = {
            "Content-Type": "application/json"
        }
        
        print(f"Sending test data to {UPDATE_RAG_ENDPOINT}")
        response = requests.post(UPDATE_RAG_ENDPOINT, json=test_data, headers=headers, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("Direct API call test successful!")
            return True
        else:
            print("Direct API call test failed!")
            return False
            
    except Exception as e:
        print(f"Error in direct API call test: {e}")
        return False

if __name__ == "__main__":
    print("Running webhook tests...")
    print("=" * 50)
    
    # Test 1: Full webhook process
    print("Test 1: Full webhook process")
    test_webhook()
    
    print("\n" + "=" * 50)
    
    # Test 2: Direct API call
    print("Test 2: Direct API call")
    test_direct_api_call()