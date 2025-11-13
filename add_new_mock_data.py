"""
Script to add new mock data to Prisma database tables
This script adds new records with unique IDs to avoid conflicts
"""

import os
import asyncio
import asyncpg
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")

async def add_new_mock_data():
    """Add new mock data to Prisma database tables"""
    try:
        # Check if DATABASE_URL is available
        if not DATABASE_URL:
            print("Error: DATABASE_URL not found in environment variables")
            return False
            
        # Connect to the database
        print("Connecting to Prisma database...")
        conn = await asyncpg.connect(DATABASE_URL)
        
        print("Database connection successful!")
        
        # Add new hospital
        print("Adding new hospital...")
        await conn.execute('''
            INSERT INTO "Hospital" (hospital_id, hospital_name, address, phone_number, created_at)
            VALUES ($1, $2, $3, $4, $5)
        ''', 'HOSP004', 'Metropolitan Medical Center', '789 Healthcare Drive, MetroCity', '+1-555-0199', datetime.now())
        
        # Add new doctor
        print("Adding new doctor...")
        await conn.execute('''
            INSERT INTO "Doctor" (doctor_id, doctor_name, hospital_id, phone_number, certificate_url, 
                                 id_document_url, profile_image_url, created_at)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
        ''', 'DOC006', 'Dr. James Wilson', 'HOSP004', '+1-555-0198', 
            'https://example.com/certificates/jwilson.pdf',
            'https://example.com/ids/jwilson.pdf',
            'https://example.com/profiles/jwilson.jpg',
            datetime.now())
        
        # Add new user (patient)
        print("Adding new patient...")
        await conn.execute('''
            INSERT INTO "User" (user_id, user_name, user_mobile, address, treated_by, hospital_id, 
                              transcripted_data, audio_url, created_at)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
        ''', 'USR006', 'Olivia Brown', '+1-555-0197', '321 Wellness Street, HealthVille', 
            'DOC006', 'HOSP004', 'Patient reports seasonal allergies and mild asthma', 
            'https://example.com/audio/olivia_brown_20231016.wav', datetime.now())
        
        # Add new interaction
        print("Adding new interaction...")
        await conn.execute('''
            INSERT INTO "Interaction" (id, doctor_id, patient_id, audio_url, transcripted_data, 
                                     soap_notes, reports_url, created_at)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
        ''', 'INT006', 'DOC006', 'USR006', 'https://example.com/audio/int_006.wav',
            'Doctor consultation regarding patient seasonal allergies and mild asthma. Patient reports symptoms for 1 month.',
            'S: Patient reports seasonal allergies and mild asthma for 1 month. O: BP 118/76, Temp 98.4F, Lungs clear. A: Allergic rhinitis with mild asthma. P: Antihistamine and inhaler.',
            'https://example.com/reports/int_006.pdf', datetime.now())
        
        # Add new report
        print("Adding new report...")
        await conn.execute('''
            INSERT INTO "Report" (id, "userId", file_url, note, created_at)
            VALUES ($1, $2, $3, $4, $5)
        ''', 'REP006', 'USR006', 'https://example.com/reports/allergy_test_006.pdf',
            'Allergy test shows sensitivity to pollen and dust mites. Lung function test normal.', datetime.now())
        
        # Add new SOAP note
        print("Adding new SOAP note...")
        await conn.execute('''
            INSERT INTO "SoapNote" (id, "userId", note, created_at)
            VALUES ($1, $2, $3, $4)
        ''', 'SOAP006', 'USR006', 'Follow-up in 3 weeks to monitor allergy symptoms. Continue current medication.', datetime.now())
        
        print("New mock data added successfully!")
        
        # Verify data insertion by counting rows in each table
        tables = ['Hospital', 'Doctor', 'User', 'Interaction', 'Report', 'SoapNote']
        print("\nUpdated row counts:")
        for table in tables:
            count = await conn.fetchval(f'SELECT COUNT(*) FROM "{table}"')
            print(f"  {table}: {count} rows")
        
        # Close connection
        await conn.close()
        
        return True
        
    except Exception as error:
        print(f"Error adding new mock data: {error}")
        return False

if __name__ == "__main__":
    print("Adding new mock data to Prisma database...")
    asyncio.run(add_new_mock_data())