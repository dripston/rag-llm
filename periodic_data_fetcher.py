"""
Periodic Data Fetcher
This script periodically checks for new data in the database and sends it to the RAG system.
"""

import asyncio
import asyncpg
import json
import os
import logging
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configuration
DATABASE_URL = os.getenv("DATABASE_URL")
RENDER_SERVICE_URL = os.getenv("RENDER_SERVICE_URL", "https://rag-llm-1.onrender.com")
UPDATE_RAG_ENDPOINT = f"{RENDER_SERVICE_URL}/update_rag"

# Track the last check time
last_check_time = None

async def send_to_rag_system(data, operation_type):
    """Send data to the RAG system"""
    try:
        headers = {
            "Content-Type": "application/json"
        }
        
        # Format the data to match what the RAG system expects
        payload = {
            "timestamp": datetime.now().isoformat(),
            "source": "periodic_fetcher",
            "operation": operation_type,
            "data": data
        }
        
        logger.info(f"Sending data to RAG system: {UPDATE_RAG_ENDPOINT}")
        logger.info(f"Payload: {payload}")
        
        # Send the request
        response = requests.post(UPDATE_RAG_ENDPOINT, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            logger.info("Successfully sent data to RAG system")
            logger.info(f"Response: {response.text}")
            return True
        else:
            logger.error(f"Failed to send data to RAG system. Status code: {response.status_code}")
            logger.error(f"Response: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Error sending data to RAG system: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False

async def check_for_new_data(conn):
    """Check for new data in all tables"""
    global last_check_time
    
    # Set the check time for this run
    current_check_time = datetime.utcnow()
    
    # If this is the first run, check for data from the last 5 minutes
    if last_check_time is None:
        last_check_time = current_check_time - timedelta(minutes=5)
    
    logger.info(f"Checking for data updated between {last_check_time} and {current_check_time}")
    
    # Check Hospital table
    try:
        hospitals = await conn.fetch('''
            SELECT * FROM "Hospital" 
            WHERE created_at > $1
            ORDER BY created_at DESC
        ''', last_check_time)
        
        if hospitals:
            logger.info(f"Found {len(hospitals)} new/updated hospitals")
            hospitals_data = []
            for hospital in hospitals:
                hospital_dict = dict(hospital)
                # Convert datetime objects to strings
                if 'created_at' in hospital_dict and hospital_dict['created_at']:
                    hospital_dict['created_at'] = hospital_dict['created_at'].isoformat()
                hospitals_data.append(hospital_dict)
            await send_to_rag_system(hospitals_data, "hospital_update")
    except Exception as e:
        logger.error(f"Error checking hospitals: {e}")
    
    # Check Doctor table
    try:
        doctors = await conn.fetch('''
            SELECT * FROM "Doctor" 
            WHERE created_at > $1
            ORDER BY created_at DESC
        ''', last_check_time)
        
        if doctors:
            logger.info(f"Found {len(doctors)} new/updated doctors")
            doctors_data = []
            for doctor in doctors:
                doctor_dict = dict(doctor)
                # Convert datetime objects to strings
                if 'created_at' in doctor_dict and doctor_dict['created_at']:
                    doctor_dict['created_at'] = doctor_dict['created_at'].isoformat()
                doctors_data.append(doctor_dict)
            await send_to_rag_system(doctors_data, "doctor_update")
    except Exception as e:
        logger.error(f"Error checking doctors: {e}")
    
    # Check User table
    try:
        users = await conn.fetch('''
            SELECT * FROM "User" 
            WHERE created_at > $1
            ORDER BY created_at DESC
        ''', last_check_time)
        
        if users:
            logger.info(f"Found {len(users)} new/updated users")
            users_data = []
            for user in users:
                user_dict = dict(user)
                # Convert datetime objects to strings
                if 'created_at' in user_dict and user_dict['created_at']:
                    user_dict['created_at'] = user_dict['created_at'].isoformat()
                users_data.append(user_dict)
            await send_to_rag_system(users_data, "user_update")
    except Exception as e:
        logger.error(f"Error checking users: {e}")
    
    # Update the last check time
    last_check_time = current_check_time

async def periodic_fetcher():
    """Main periodic fetcher loop"""
    conn = None
    
    try:
        # Connect to the database
        logger.info("Connecting to PostgreSQL database...")
        conn = await asyncpg.connect(DATABASE_URL)
        logger.info("Connected to PostgreSQL database")
        
        # Run the periodic check
        while True:
            try:
                logger.info("Checking for new data...")
                await check_for_new_data(conn)
                logger.info("Check completed. Waiting for next check...")
                
                # Wait for 1 second before next check
                await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f"Error in periodic check: {e}")
                import traceback
                logger.error(f"Traceback: {traceback.format_exc()}")
                # Wait a bit before retrying
                await asyncio.sleep(5)
                
    except KeyboardInterrupt:
        logger.info("Stopping periodic fetcher...")
    except Exception as e:
        logger.error(f"Error in periodic fetcher: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
    finally:
        if conn:
            await conn.close()
            logger.info("Database connection closed")

if __name__ == "__main__":
    logger.info("Starting periodic data fetcher...")
    asyncio.run(periodic_fetcher())