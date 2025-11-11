import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Supabase project configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def test_supabase_connection():
    """Test the Supabase connection using the official client library"""
    try:
        # Check if environment variables are loaded
        if not SUPABASE_URL or not SUPABASE_KEY:
            print("Error: SUPABASE_URL or SUPABASE_KEY not found in environment variables")
            return False
            
        # Create Supabase client
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        print("Supabase client created successfully!")
        
        # Test authentication by getting user info (this will work with anon key)
        # Note: This doesn't actually fetch user data but tests the connection
        
        # Try to access the medical_records table to see if it exists
        try:
            # Attempt to get table info
            response = supabase.table('medical_records').select("count").execute()
            print("✓ Connected to 'medical_records' table")
            print(f"  Query executed successfully")
        except Exception as table_error:
            print(f"✗ Error accessing 'medical_records' table: {table_error}")
        
        # Try to access the soap_notes table
        try:
            response = supabase.table('soap_notes').select("count").execute()
            print("✓ Connected to 'soap_notes' table")
            print(f"  Query executed successfully")
        except Exception as table_error:
            print(f"✗ Error accessing 'soap_notes' table: {table_error}")
            
        return True
        
    except Exception as error:
        print(f"Error creating Supabase client: {error}")
        return False

if __name__ == "__main__":
    print("Testing Supabase connection...")
    test_supabase_connection()