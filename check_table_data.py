import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Supabase project configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def check_table_data():
    """Check data in the medical_records and soap_notes tables"""
    try:
        # Check if environment variables are loaded
        if not SUPABASE_URL or not SUPABASE_KEY:
            print("Error: SUPABASE_URL or SUPABASE_KEY not found in environment variables")
            return
            
        # Create Supabase client
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        print("Checking data in medical_records table...")
        try:
            # Get all records from medical_records
            response = supabase.table('medical_records').select("*").execute()
            records = response.data
            
            print(f"Found {len(records)} records in medical_records table")
            
            # Display first 3 records as examples
            for i, record in enumerate(records[:3]):
                print(f"\nRecord {i+1}:")
                for key, value in record.items():
                    print(f"  {key}: {value}")
                    
        except Exception as error:
            print(f"Error querying medical_records table: {error}")
        
        print("\n" + "="*50 + "\n")
        
        print("Checking data in soap_notes table...")
        try:
            # Get all records from soap_notes
            response = supabase.table('soap_notes').select("*").execute()
            notes = response.data
            
            print(f"Found {len(notes)} records in soap_notes table")
            
            # Display first 3 records as examples
            for i, note in enumerate(notes[:3]):
                print(f"\nNote {i+1}:")
                for key, value in note.items():
                    print(f"  {key}: {value}")
                    
        except Exception as error:
            print(f"Error querying soap_notes table: {error}")
            
    except Exception as error:
        print(f"Error creating Supabase client: {error}")

if __name__ == "__main__":
    print("Checking table data in Supabase...")
    check_table_data()