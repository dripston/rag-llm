import os
import asyncio
import asyncpg
import logging
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
import json

# Set up logging
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")

async def fetch_prisma_data():
    """Fetch data from all Prisma database tables"""
    try:
        # Check if DATABASE_URL is available
        if not DATABASE_URL:
            logger.error("DATABASE_URL not found in environment variables")
            return {}, []
            
        # Connect to the database
        logger.info("Connecting to Prisma database...")
        conn = await asyncpg.connect(DATABASE_URL)
        
        logger.info("Database connection successful!")
        
        # Fetch data from all tables
        data = {}
        
        # Fetch Hospitals
        logger.info("Fetching Hospital data...")
        hospitals = await conn.fetch('SELECT * FROM "Hospital"')
        data['hospitals'] = [dict(record) for record in hospitals]
        logger.info(f"  Found {len(hospitals)} hospitals")
        
        # Fetch Doctors
        logger.info("Fetching Doctor data...")
        doctors = await conn.fetch('SELECT * FROM "Doctor"')
        data['doctors'] = [dict(record) for record in doctors]
        logger.info(f"  Found {len(doctors)} doctors")
        
        # Fetch Users (Patients)
        logger.info("Fetching User (Patient) data...")
        users = await conn.fetch('SELECT * FROM "User"')
        data['users'] = [dict(record) for record in users]
        logger.info(f"  Found {len(users)} users")
        
        # Fetch Interactions
        logger.info("Fetching Interaction data...")
        interactions = await conn.fetch('SELECT * FROM "Interaction"')
        data['interactions'] = [dict(record) for record in interactions]
        logger.info(f"  Found {len(interactions)} interactions")
        
        # Fetch Reports
        logger.info("Fetching Report data...")
        reports = await conn.fetch('SELECT * FROM "Report"')
        data['reports'] = [dict(record) for record in reports]
        logger.info(f"  Found {len(reports)} reports")
        
        # Fetch SOAP Notes
        logger.info("Fetching SOAP Note data...")
        soap_notes = await conn.fetch('SELECT * FROM "SoapNote"')
        data['soap_notes'] = [dict(record) for record in soap_notes]
        logger.info(f"  Found {len(soap_notes)} SOAP notes")
        
        # Close connection
        await conn.close()
        
        return data
        
    except Exception as error:
        logger.error(f"Error fetching data: {error}")
        return {}

def convert_to_documents(data):
    """Convert fetched data to LangChain Documents"""
    documents = []
    
    # Handle case where data might be empty or malformed
    if not data or not isinstance(data, dict):
        logger.warning("No valid data provided for document conversion")
        return documents
    
    # Convert Hospitals to documents
    for hospital in data.get('hospitals', []):
        content = f"""
        Hospital Information:
        ID: {hospital['hospital_id']}
        Name: {hospital['hospital_name']}
        Address: {hospital['address']}
        Phone: {hospital['phone_number']}
        Created: {hospital['created_at']}
        """
        
        metadata = {
            "source": "hospital",
            "hospital_id": hospital['hospital_id'],
            "created_at": str(hospital['created_at'])
        }
        
        doc = Document(page_content=content.strip(), metadata=metadata)
        documents.append(doc)
    
    # Convert Doctors to documents
    for doctor in data.get('doctors', []):
        content = f"""
        Doctor Information:
        ID: {doctor['doctor_id']}
        Name: {doctor['doctor_name']}
        Hospital ID: {doctor['hospital_id']}
        Phone: {doctor['phone_number']}
        Certificate URL: {doctor['certificate_url']}
        ID Document URL: {doctor['id_document_url']}
        Profile Image URL: {doctor['profile_image_url']}
        Created: {doctor['created_at']}
        """
        
        metadata = {
            "source": "doctor",
            "doctor_id": doctor['doctor_id'],
            "hospital_id": doctor['hospital_id'],
            "created_at": str(doctor['created_at'])
        }
        
        doc = Document(page_content=content.strip(), metadata=metadata)
        documents.append(doc)
    
    # Convert Users (Patients) to documents
    for user in data.get('users', []):
        content = f"""
        Patient Information:
        ID: {user['user_id']}
        Name: {user['user_name']}
        Mobile: {user['user_mobile']}
        Address: {user['address']}
        Treated By: {user['treated_by']}
        Hospital ID: {user['hospital_id']}
        Transcript: {user['transcripted_data']}
        Audio URL: {user['audio_url']}
        Created: {user['created_at']}
        """
        
        metadata = {
            "source": "user",
            "user_id": user['user_id'],
            "treated_by": user['treated_by'],
            "hospital_id": user['hospital_id'],
            "created_at": str(user['created_at'])
        }
        
        doc = Document(page_content=content.strip(), metadata=metadata)
        documents.append(doc)
    
    # Convert Interactions to documents
    for interaction in data.get('interactions', []):
        content = f"""
        Doctor-Patient Interaction:
        ID: {interaction['id']}
        Doctor ID: {interaction['doctor_id']}
        Patient ID: {interaction['patient_id']}
        Audio URL: {interaction['audio_url']}
        Transcript: {interaction['transcripted_data']}
        SOAP Notes: {interaction['soap_notes']}
        Reports URL: {interaction['reports_url']}
        Created: {interaction['created_at']}
        """
        
        metadata = {
            "source": "interaction",
            "interaction_id": interaction['id'],
            "doctor_id": interaction['doctor_id'],
            "patient_id": interaction['patient_id'],
            "created_at": str(interaction['created_at'])
        }
        
        doc = Document(page_content=content.strip(), metadata=metadata)
        documents.append(doc)
    
    # Convert Reports to documents
    for report in data.get('reports', []):
        content = f"""
        Medical Report:
        ID: {report['id']}
        Patient ID: {report['userId']}
        File URL: {report['file_url']}
        Note: {report['note']}
        Created: {report['created_at']}
        """
        
        metadata = {
            "source": "report",
            "report_id": report['id'],
            "user_id": report['userId'],
            "created_at": str(report['created_at'])
        }
        
        doc = Document(page_content=content.strip(), metadata=metadata)
        documents.append(doc)
    
    # Convert SOAP Notes to documents
    for soap_note in data.get('soap_notes', []):
        content = f"""
        SOAP Note:
        ID: {soap_note['id']}
        Patient ID: {soap_note['userId']}
        Note Content: {soap_note['note']}
        Created: {soap_note['created_at']}
        """
        
        metadata = {
            "source": "soap_note",
            "soap_id": soap_note['id'],
            "user_id": soap_note['userId'],
            "created_at": str(soap_note['created_at'])
        }
        
        doc = Document(page_content=content.strip(), metadata=metadata)
        documents.append(doc)
    
    logger.info(f"Converted {len(documents)} documents from provided data")
    return documents

def chunk_documents(documents):
    """Chunk documents using LangChain's RecursiveCharacterTextSplitter"""
    # Initialize the text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        separators=["\n\n", "\n", ". ", "! ", "? ", " ", ""]
    )
    
    # Split documents into chunks
    chunked_documents = text_splitter.split_documents(documents)
    
    return chunked_documents

async def main():
    """Main function to fetch data, convert to documents, and chunk them"""
    logger.info("Fetching medical data from Prisma database...")
    data = await fetch_prisma_data()
    
    if not data:
        logger.error("Failed to fetch data. Exiting.")
        return []
    
    logger.info("Converting records to LangChain Documents...")
    documents = convert_to_documents(data)
    
    logger.info(f"Created {len(documents)} documents")
    
    logger.info("Chunking documents...")
    chunked_documents = chunk_documents(documents)
    
    logger.info(f"Created {len(chunked_documents)} chunks")
    
    # Display information about the first few chunks
    logger.info("\nFirst 3 chunks:")
    for i, chunk in enumerate(chunked_documents[:3]):
        logger.info(f"\nChunk {i+1}:")
        logger.info(f"Content length: {len(chunk.page_content)} characters")
        logger.info(f"Metadata: {chunk.metadata}")
        logger.info("Content preview:")
        logger.info(chunk.page_content[:300] + "..." if len(chunk.page_content) > 300 else chunk.page_content)
        logger.info("-" * 50)
    
    # Save chunks to a file for inspection
    chunk_data = []
    for chunk in chunked_documents:
        chunk_data.append({
            "content": chunk.page_content,
            "metadata": chunk.metadata
        })
    
    with open("chunked_prisma_data.json", "w", encoding="utf-8") as f:
        json.dump(chunk_data, f, indent=2, default=str)
    
    logger.info(f"\nAll chunks saved to 'chunked_prisma_data.json'")
    
    return chunked_documents

if __name__ == "__main__":
    # Set up logging for standalone execution
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())