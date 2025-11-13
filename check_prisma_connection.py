import os
import asyncio
import asyncpg
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")

async def check_table_structure():
    """Check the structure of tables in the Prisma database"""
    try:
        # Check if DATABASE_URL is available
        if not DATABASE_URL:
            print("Error: DATABASE_URL not found in environment variables")
            return False
            
        # Connect to the database
        print("Connecting to Prisma database...")
        conn = await asyncpg.connect(DATABASE_URL)
        
        print("Database connection successful!")
        
        # List all tables in the database
        print("Checking table structures...")
        tables = await conn.fetch("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name != '_prisma_migrations'
            ORDER BY table_name;
        """)
        
        for table in tables:
            table_name = table['table_name']
            print(f"\nTable: {table_name}")
            
            # Get column information
            columns = await conn.fetch("""
                SELECT column_name, data_type, is_nullable 
                FROM information_schema.columns 
                WHERE table_name = $1 AND table_schema = 'public'
                ORDER BY ordinal_position;
            """, table_name)
            
            for column in columns:
                print(f"  {column['column_name']} ({column['data_type']}) {'NULL' if column['is_nullable'] == 'YES' else 'NOT NULL'}")
        
        # Close connection
        await conn.close()
        
        return True
        
    except Exception as error:
        print(f"Error connecting to database: {error}")
        return False

if __name__ == "__main__":
    print("Checking Prisma database table structures...")
    asyncio.run(check_table_structure())