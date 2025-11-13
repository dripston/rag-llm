"""
Script to execute the Prisma database triggers SQL file
"""

import os
import asyncio
import asyncpg
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")

async def execute_triggers():
    """Execute the triggers SQL file against the database"""
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
        with open('prisma_triggers.sql', 'r') as file:
            sql_commands = file.read()
        
        # Execute SQL commands
        print("Executing triggers SQL commands...")
        await conn.execute(sql_commands)
        
        print("Database triggers created successfully!")
        
        # Close connection
        await conn.close()
        
        return True
        
    except Exception as error:
        print(f"Error executing triggers: {error}")
        return False

if __name__ == "__main__":
    print("Executing Prisma database triggers...")
    asyncio.run(execute_triggers())