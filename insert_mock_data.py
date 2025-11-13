import os
import asyncio
import asyncpg
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")

async def insert_mock_data():
    """Insert mock data into Prisma database tables"""
    try:
        # Check if DATABASE_URL is available
        if not DATABASE_URL:
            print("Error: DATABASE_URL not found in environment variables")
            return False
            
        # Connect to the database
        print("Connecting to Prisma database...")
        conn = await asyncpg.connect(DATABASE_URL)
        
        print("Database connection successful!")
        
        # Read SQL file
        with open('insert_mock_data.sql', 'r') as file:
            sql_commands = file.read()
        
        # Execute SQL commands
        print("Inserting mock data...")
        await conn.execute(sql_commands)
        
        print("Mock data inserted successfully!")
        
        # Verify data insertion by counting rows in each table
        tables = ['Hospital', 'Doctor', 'User', 'Interaction', 'Report', 'SoapNote']
        for table in tables:
            count = await conn.fetchval(f'SELECT COUNT(*) FROM "{table}"')
            print(f"  {table}: {count} rows")
        
        # Close connection
        await conn.close()
        
        return True
        
    except Exception as error:
        print(f"Error inserting mock data: {error}")
        return False

if __name__ == "__main__":
    print("Inserting mock data into Prisma database...")
    asyncio.run(insert_mock_data())