import psycopg2
from psycopg2 import sql
import os

# Supabase database connection parameters
DB_HOST = "bubvzeylnvznjlzcalgx.supabase.co"  # Fixed: removed 'db.' prefix
DB_NAME = "postgres"
DB_USER = "postgres.bubvzeylnvznjlzcalgx"
DB_PASSWORD = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJ1YnZ6ZXlsbnZ6bmpsemNhbGd4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI4NjY5NzgsImV4cCI6MjA3ODQ0Mjk3OH0.CUaoAyzyCVBqM27qqsty2FZpoj-9F0uItIWlNCMxVRU"
DB_PORT = "5432"

def test_connection():
    """Test the database connection"""
    try:
        # Establish connection
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        
        # Create cursor
        cur = conn.cursor()
        
        # Execute a simple query
        cur.execute("SELECT version();")
        db_version = cur.fetchone()
        
        print("Database connection successful!")
        if db_version:
            print(f"PostgreSQL version: {db_version[0]}")
        
        # Check if our tables exist
        tables_to_check = ['medical_records', 'soap_notes']
        
        for table in tables_to_check:
            cur.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = %s
                );
            """, (table,))
            
            result = cur.fetchone()
            exists = result[0] if result else False
            if exists:
                print(f"✓ Table '{table}' exists")
                
                # Count rows in the table
                cur.execute(sql.SQL("SELECT COUNT(*) FROM {}").format(sql.Identifier(table)))
                count_result = cur.fetchone()
                count = count_result[0] if count_result else 0
                print(f"  Rows in '{table}': {count}")
            else:
                print(f"✗ Table '{table}' does not exist")
        
        # Close connections
        cur.close()
        conn.close()
        
        return True
        
    except Exception as error:
        print(f"Error connecting to database: {error}")
        return False

if __name__ == "__main__":
    print("Testing Supabase database connection...")
    test_connection()