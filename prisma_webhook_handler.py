"""
Script to handle Prisma database updates and send them to the Render RAG endpoint.
This script can be triggered by database triggers or scheduled to run periodically.
"""

import os
import json
import requests
import logging
from dotenv import load_dotenv
import asyncio
from chunk_prisma_data import fetch_prisma_data
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configuration
RENDER_SERVICE_URL = os.getenv("RENDER_SERVICE_URL", "https://rag-llm-1.onrender.com")
UPDATE_RAG_ENDPOINT = f"{RENDER_SERVICE_URL}/update_rag"

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")

# Custom JSON encoder to handle datetime objects
class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)

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
        
        logger.info(f"Sending data to Render endpoint: {UPDATE_RAG_ENDPOINT}")
        # Use the custom encoder to handle datetime objects
        response = requests.post(UPDATE_RAG_ENDPOINT, data=json.dumps(payload, cls=DateTimeEncoder), headers=headers, timeout=30)
        
        if response.status_code == 200:
            logger.info("Successfully sent data to Render RAG endpoint")
            return True
        else:
            logger.error(f"Failed to send data to Render. Status code: {response.status_code}")
            logger.error(f"Response: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Error sending data to Render: {e}")
        return False

async def fetch_and_send_updates():
    """Fetch new data from Prisma and send to Render"""
    try:
        logger.info("Fetching new data from Prisma database...")
        data = await fetch_prisma_data()
        
        if not data:
            logger.warning("No new data found")
            return False
            
        # Count records properly
        record_count = 0
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, list):
                    record_count += len(value)
        logger.info(f"Fetched {record_count} records from database")
        
        # Send data to Render
        success = await send_update_to_render(data)
        
        if success:
            logger.info("Successfully updated RAG system on Render")
        else:
            logger.error("Failed to update RAG system on Render")
            
        return success
        
    except Exception as e:
        logger.error(f"Error fetching and sending updates: {e}")
        return False

def trigger_rag_update():
    """Trigger RAG update from Prisma database to Render endpoint"""
    try:
        logger.info("Starting Prisma to Render RAG update process...")
        result = asyncio.run(fetch_and_send_updates())
        return result
    except Exception as e:
        logger.error(f"Error in trigger_rag_update: {e}")
        return False

if __name__ == "__main__":
    # Run the update process
    trigger_rag_update()