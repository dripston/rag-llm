import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Pinecone configuration
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

print("Pinecone API Key:", PINECONE_API_KEY[:10] if PINECONE_API_KEY else "Not found")