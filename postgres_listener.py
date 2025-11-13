"""
PostgreSQL Listener for RAG System Updates
This script listens for PostgreSQL notifications and forwards them to the RAG system.
"""

import asyncio
import asyncpg
import json
import os
from dotenv import load_dotenv
import requests
from datetime import datetime

# Load environment variables
load_dotenv()

# Configuration
DATABASE_URL = os.getenv("DATABASE_URL")
RENDER_SERVICE_URL = os.getenv("RENDER_SERVICE_URL", "https://rag-llm-1.onrender.com")
UPDATE_RAG_ENDPOINT = f"{RENDER_SERVICE_URL}/update_rag"

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
        
        print(f"Sending data to RAG system: {UPDATE_RAG_ENDPOINT}")
        response = requests.post(UPDATE_RAG_ENDPOINT, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            print("Successfully sent data to RAG system")
            return True
        else:
            print(f"Failed to send data to RAG system. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error sending data to RAG system: {e}")
        return False

async def listen_for_notifications():
    """Listen for PostgreSQL notifications"""
    try:
        # Connect to the database
        conn = await asyncpg.connect(DATABASE_URL)
        print("Connected to PostgreSQL database")
        
        # Listen for RAG update notifications
        await conn.add_listener('rag_update', handle_notification)
        print("Listening for 'rag_update' notifications...")
        print("Press Ctrl+C to stop")
        
        # Keep the connection alive
        while True:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        print("\nStopping listener...")
    except Exception as e:
        print(f"Error in listener: {e}")
    finally:
        if 'conn' in locals():
            await conn.close()
            print("Database connection closed")

def handle_notification(connection, pid, channel, payload):
    """Handle incoming PostgreSQL notifications"""
    try:
        print(f"Received notification on channel '{channel}': {payload}")
        
        # Parse the payload
        if payload:
            data = json.loads(payload)
            print(f"Parsed data: {data}")
            
            # Send to RAG system
            # Note: We need to run this in a new event loop since we're in a synchronous callback
            asyncio.create_task(send_to_rag_system(data))
        else:
            print("Received empty notification payload")
            
    except json.JSONDecodeError:
        print(f"Failed to parse notification payload as JSON: {payload}")
    except Exception as e:
        print(f"Error handling notification: {e}")

async def main():
    """Main function"""
    print("Starting PostgreSQL listener for RAG system updates...")
    await listen_for_notifications()

if __name__ == "__main__":
    asyncio.run(main())