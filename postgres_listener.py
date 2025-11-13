"""
PostgreSQL Listener for RAG System Updates
This script listens for PostgreSQL notifications and forwards them to the RAG system.
"""

import asyncio
import asyncpg
import json
import os
import logging
from dotenv import load_dotenv
import requests
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configuration
DATABASE_URL = os.getenv("DATABASE_URL")
RENDER_SERVICE_URL = os.getenv("RENDER_SERVICE_URL", "https://rag-llm-1.onrender.com")
UPDATE_RAG_ENDPOINT = f"{RENDER_SERVICE_URL}/update_rag"

# Global event loop reference
event_loop = None

async def send_to_rag_system(data):
    """Send data to the RAG system"""
    try:
        headers = {
            "Content-Type": "application/json"
        }
        
        payload = {
            "timestamp": datetime.now().isoformat(),
            "source": "postgres_trigger",
            "data": data
        }
        
        logger.info(f"Sending data to RAG system: {UPDATE_RAG_ENDPOINT}")
        response = requests.post(UPDATE_RAG_ENDPOINT, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            logger.info("Successfully sent data to RAG system")
            return True
        else:
            logger.error(f"Failed to send data to RAG system. Status code: {response.status_code}")
            logger.error(f"Response: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Error sending data to RAG system: {e}")
        return False

async def listen_for_notifications():
    """Listen for PostgreSQL notifications"""
    global event_loop
    event_loop = asyncio.get_event_loop()
    
    # Initialize connection variable
    conn = None
    
    try:
        # Connect to the database
        conn = await asyncpg.connect(DATABASE_URL)
        logger.info("Connected to PostgreSQL database")
        
        # Listen for RAG update notifications
        await conn.add_listener('rag_update', handle_notification)
        logger.info("Listening for 'rag_update' notifications...")
        logger.info("Press Ctrl+C to stop")
        
        # Keep the connection alive
        while True:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("\nStopping listener...")
    except Exception as e:
        logger.error(f"Error in listener: {e}")
    finally:
        if conn:
            await conn.close()
            logger.info("Database connection closed")

def handle_notification(connection, pid, channel, payload):
    """Handle incoming PostgreSQL notifications"""
    try:
        logger.info(f"Received notification on channel '{channel}': {payload}")
        
        # Parse the payload
        if payload:
            data = json.loads(payload)
            logger.info(f"Parsed data: {data}")
            
            # Send to RAG system using the global event loop
            if event_loop:
                asyncio.run_coroutine_threadsafe(send_to_rag_system(data), event_loop)
        else:
            logger.warning("Received empty notification payload")
            
    except json.JSONDecodeError:
        logger.error(f"Failed to parse notification payload as JSON: {payload}")
    except Exception as e:
        logger.error(f"Error handling notification: {e}")

async def main():
    """Main function"""
    logger.info("Starting PostgreSQL listener for RAG system updates...")
    await listen_for_notifications()

if __name__ == "__main__":
    asyncio.run(main())