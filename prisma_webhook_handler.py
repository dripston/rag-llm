"""
Script to handle Prisma database updates and send them to the Render RAG endpoint.
This script can be triggered by database triggers or scheduled to run periodically.
"""

import os
import json
import requests
from dotenv import load_dotenv
import asyncio
from chunk_prisma_data import fetch_prisma_data
from datetime import datetime

# Load environment variables
load_dotenv()

# Configuration
RENDER_SERVICE_URL = os.getenv("RENDER_SERVICE_URL", "https://rag-llm-1.onrender.com")
UPDATE_RAG_ENDPOINT = f"{RENDER_SERVICE_URL}/update_rag"

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")

async def send_update_to_render(data):
    """Send updated data to the Render RAG endpoint"""
    try:
        headers = {
            "Content-Type": "application/json"
        }
        
        payload = {
            "timestamp": datetime.now().isoformat(),
            "data": data,
            "source": "prisma_database"
        }
        
        print(f"Sending data to Render endpoint: {UPDATE_RAG_ENDPOINT}")
        response = requests.post(UPDATE_RAG_ENDPOINT, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            print("Successfully sent data to Render RAG endpoint")
            return True
        else:
            print(f"Failed to send data to Render. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error sending data to Render: {e}")
        return False

async def fetch_and_send_updates():
    """Fetch new data from Prisma and send to Render"""
    try:
        print("Fetching new data from Prisma database...")
        data = await fetch_prisma_data()
        
        if not data:
            print("No new data found")
            return False
            
        print(f"Fetched {sum(len(v) for v in data.values())} records from database")
        
        # Send data to Render
        success = await send_update_to_render(data)
        
        if success:
            print("Successfully updated RAG system on Render")
        else:
            print("Failed to update RAG system on Render")
            
        return success
        
    except Exception as e:
        print(f"Error fetching and sending updates: {e}")
        return False

def trigger_rag_update():
    """Trigger RAG update from Prisma database to Render endpoint"""
    try:
        print("Starting Prisma to Render RAG update process...")
        result = asyncio.run(fetch_and_send_updates())
        return result
    except Exception as e:
        print(f"Error in trigger_rag_update: {e}")
        return False

if __name__ == "__main__":
    # Run the update process
    trigger_rag_update()