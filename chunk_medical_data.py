import os
from supabase import create_client, Client
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Supabase project configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def fetch_medical_data():
    """Fetch data from medical_records and soap_notes tables"""
    try:
        # Check if environment variables are loaded
        if not SUPABASE_URL or not SUPABASE_KEY:
            print("Error: SUPABASE_URL or SUPABASE_KEY not found in environment variables")
            return [], []
        
        # Create Supabase client
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Fetch medical records
        medical_response = supabase.table('medical_records').select("*").execute()
        medical_records = medical_response.data
        
        # Fetch SOAP notes
        soap_response = supabase.table('soap_notes').select("*").execute()
        soap_notes = soap_response.data
        
        return medical_records, soap_notes
        
    except Exception as error:
        print(f"Error fetching data: {error}")
        return [], []

def convert_records_to_documents(medical_records, soap_notes):
    """Convert medical records and SOAP notes to LangChain Documents"""
    documents = []
    
    # Convert medical records to documents
    for record in medical_records:
        # Create a comprehensive text representation of the medical record
        content = f"""
        Patient ID: {record['user_id']}
        Patient Name: {record['user_name']}
        Doctor: {record['treated_by']}
        Hospital ID: {record['hospital_id']}
        Mobile: {record['user_mobile']}
        Address: {record['address']}
        Transcript: {record['transcripted_data']}
        Audio URL: {record['audio_url']}
        Record Date: {record['created_at']}
        """
        
        # Create metadata for the document
        metadata = {
            "source": "medical_record",
            "user_id": record['user_id'],
            "user_name": record['user_name'],
            "doctor": record['treated_by'],
            "hospital_id": record['hospital_id'],
            "created_at": record['created_at']
        }
        
        doc = Document(page_content=content.strip(), metadata=metadata)
        documents.append(doc)
    
    # Convert SOAP notes to documents and link to medical records
    for note in soap_notes:
        # Create a comprehensive text representation of the SOAP note
        content = f"""
        SOAP Note ID: {note['id']}
        Patient ID: {note['medical_record_id']}
        Subjective: {note['subjective']}
        Objective: {note['objective']}
        Assessment: {note['assessment']}
        Plan: {note['plan']}
        Note Date: {note['created_at']}
        """
        
        # Find the corresponding medical record to get patient info
        patient_name = "Unknown"
        doctor = "Unknown"
        for record in medical_records:
            if record['user_id'] == note['medical_record_id']:
                patient_name = record['user_name']
                doctor = record['treated_by']
                break
        
        # Create metadata for the document
        metadata = {
            "source": "soap_note",
            "note_id": note['id'],
            "user_id": note['medical_record_id'],
            "user_name": patient_name,
            "doctor": doctor,
            "created_at": note['created_at']
        }
        
        doc = Document(page_content=content.strip(), metadata=metadata)
        documents.append(doc)
    
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

def main():
    """Main function to fetch data, convert to documents, and chunk them"""
    print("Fetching medical data from Supabase...")
    medical_records, soap_notes = fetch_medical_data()
    
    if not medical_records and not soap_notes:
        print("Failed to fetch data. Exiting.")
        return []
    
    print(f"Fetched {len(medical_records)} medical records and {len(soap_notes)} SOAP notes")
    
    print("Converting records to LangChain Documents...")
    documents = convert_records_to_documents(medical_records, soap_notes)
    
    print(f"Created {len(documents)} documents")
    
    print("Chunking documents...")
    chunked_documents = chunk_documents(documents)
    
    print(f"Created {len(chunked_documents)} chunks")
    
    # Display information about the first few chunks
    print("\nFirst 3 chunks:")
    for i, chunk in enumerate(chunked_documents[:3]):
        print(f"\nChunk {i+1}:")
        print(f"Content length: {len(chunk.page_content)} characters")
        print(f"Metadata: {chunk.metadata}")
        print("Content preview:")
        print(chunk.page_content[:300] + "..." if len(chunk.page_content) > 300 else chunk.page_content)
        print("-" * 50)
    
    # Save chunks to a file for inspection
    chunk_data = []
    for chunk in chunked_documents:
        chunk_data.append({
            "content": chunk.page_content,
            "metadata": chunk.metadata
        })
    
    with open("chunked_medical_data.json", "w", encoding="utf-8") as f:
        json.dump(chunk_data, f, indent=2, default=str)
    
    print(f"\nAll chunks saved to 'chunked_medical_data.json'")
    
    return chunked_documents

if __name__ == "__main__":
    main()