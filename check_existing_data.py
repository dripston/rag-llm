"""
Script to check existing data in Prisma database tables
"""

import os
import asyncio
import asyncpg
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")

async def check_existing_data():
    """Check existing data in Prisma database tables"""
    try:
        # Check if DATABASE_URL is available
        if not DATABASE_URL:
            print("Error: DATABASE_URL not found in environment variables")
            return False
            
        # Connect to the database
        print("Connecting to Prisma database...")
        conn = await asyncpg.connect(DATABASE_URL)
        
        print("Database connection successful!")
        
        # Check existing hospitals
        print("\n--- Existing Hospitals ---")
        hospitals = await conn.fetch('SELECT hospital_id, hospital_name FROM "Hospital"')
        for hospital in hospitals:
            print(f"  {hospital['hospital_id']}: {hospital['hospital_name']}")
        
        # Check existing doctors
        print("\n--- Existing Doctors ---")
        doctors = await conn.fetch('SELECT doctor_id, doctor_name FROM "Doctor"')
        for doctor in doctors:
            print(f"  {doctor['doctor_id']}: {doctor['doctor_name']}")
        
        # Check existing users
        print("\n--- Existing Users ---")
        users = await conn.fetch('SELECT user_id, user_name FROM "User"')
        for user in users:
            print(f"  {user['user_id']}: {user['user_name']}")
        
        # Check existing interactions
        print("\n--- Existing Interactions ---")
        interactions = await conn.fetch('SELECT id, patient_id, doctor_id FROM "Interaction"')
        for interaction in interactions:
            print(f"  {interaction['id']}: Patient {interaction['patient_id']}, Doctor {interaction['doctor_id']}")
        
        # Check existing reports
        print("\n--- Existing Reports ---")
        reports = await conn.fetch('SELECT id, "userId" FROM "Report"')
        for report in reports:
            print(f"  {report['id']}: User {report['userId']}")
        
        # Check existing SOAP notes
        print("\n--- Existing SOAP Notes ---")
        soap_notes = await conn.fetch('SELECT id, "userId" FROM "SoapNote"')
        for soap_note in soap_notes:
            print(f"  {soap_note['id']}: User {soap_note['userId']}")
        
        # Close connection
        await conn.close()
        
        return True
        
    except Exception as error:
        print(f"Error checking existing data: {error}")
        return False

if __name__ == "__main__":
    print("Checking existing data in Prisma database...")
    asyncio.run(check_existing_data())