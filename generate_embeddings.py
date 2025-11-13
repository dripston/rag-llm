import os
import json
import requests
from dotenv import load_dotenv
import numpy as np
import time

# Load environment variables
load_dotenv()

# Sambanova API configuration
SAMBANOVA_API_KEY = os.getenv("SAMBANOVA_API_KEY")
SAMBANOVA_BASE_URL = os.getenv("SAMBANOVA_BASE_URL")
FALLBACK_API_KEYS = [
    os.getenv("FALLBACK_API_KEY_1"),
    os.getenv("FALLBACK_API_KEY_2"),
    os.getenv("FALLBACK_API_KEY_3"),
    os.getenv("FALLBACK_API_KEY_4"),
    os.getenv("FALLBACK_API_KEY_5")
]

def get_sambanova_embedding(text, api_key=None):
    """Generate embedding for a text using Sambanova API with fallback keys"""
    # Use provided API key or default one
    current_api_key = api_key if api_key else SAMBANOVA_API_KEY
    
    try:
        headers = {
            "Authorization": f"Bearer {current_api_key}",
            "Content-Type": "application/json"
        }
        
        # Use the correct model name
        payload = {
            "model": "E5-Mistral-7B-Instruct",
            "input": text
        }
        
        # Try the standard embeddings endpoint
        url = f"{SAMBANOVA_BASE_URL}/embeddings"
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            return data['data'][0]['embedding']
        elif response.status_code == 429:
            # Rate limit hit
            key_display = current_api_key[:8] if current_api_key else "Unknown"
            print(f"Rate limit hit with API key: {key_display}...")
            return None
        else:
            key_display = current_api_key[:8] if current_api_key else "Unknown"
            print(f"Error with API key {key_display}...: {response.status_code} - {response.text}")
            return None
            
    except Exception as error:
        key_display = current_api_key[:8] if current_api_key else "Unknown"
        print(f"Error generating embedding with API key {key_display}...: {error}")
        return None

def get_embedding_with_fallback(text):
    """Try to get embedding using primary key, then fallback keys"""
    # Try primary API key first
    embedding = get_sambanova_embedding(text)
    if embedding is not None:
        return embedding
    
    # Try fallback API keys
    for i, fallback_key in enumerate(FALLBACK_API_KEYS):
        if fallback_key:
            print(f"Trying fallback API key {i+1}...")
            embedding = get_sambanova_embedding(text, fallback_key)
            if embedding is not None:
                print(f"  ✓ Success with fallback API key {i+1}")
                return embedding
            time.sleep(1)  # Small delay between attempts
    
    return None

def load_existing_embeddings():
    """Load existing embeddings if they exist and are valid"""
    try:
        if os.path.exists("embedded_prisma_data.json"):
            with open("embedded_prisma_data.json", "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:  # Check if file is not empty
                    data = json.loads(content)
                    if isinstance(data, list):  # Check if it's a list
                        return data
                    else:
                        print("Existing embeddings file has invalid format")
                        return []
                else:
                    print("Existing embeddings file is empty")
                    return []
        return []
    except json.JSONDecodeError as json_error:
        print(f"Error parsing existing embeddings JSON: {json_error}")
        # Try to salvage what we can or start fresh
        return []
    except Exception as error:
        print(f"Error loading existing embeddings: {error}")
        return []

def generate_embeddings_for_chunks():
    """Generate embeddings for all chunked data"""
    try:
        # Load chunked data
        print("Loading chunked data...")
        with open("chunked_prisma_data.json", "r", encoding="utf-8") as f:
            chunks = json.load(f)
        
        # Load existing embeddings
        existing_embeddings = load_existing_embeddings()
        processed_count = len(existing_embeddings)
        
        print(f"Found {len(chunks)} chunks to process")
        print(f"Already processed: {processed_count} chunks")
        
        # If all chunks are already processed, we're done
        if processed_count >= len(chunks):
            print("All chunks already processed!")
            return existing_embeddings
        
        # Start from where we left off
        start_index = processed_count
        print(f"Starting from chunk {start_index + 1}")
        
        # Process remaining chunks
        for i in range(start_index, len(chunks)):
            chunk = chunks[i]
            print(f"Generating embedding for chunk {i+1}/{len(chunks)}...")
            
            # Add small delay to avoid rate limits
            time.sleep(0.5)
            
            # Get embedding for the chunk content using fallback mechanism
            embedding = get_embedding_with_fallback(chunk['content'])
            
            if embedding is not None:
                # Add embedding to chunk data
                embedded_chunk = {
                    "content": chunk['content'],
                    "metadata": chunk['metadata'],
                    "embedding": embedding
                }
                existing_embeddings.append(embedded_chunk)
                print(f"  ✓ Embedding generated (dimension: {len(embedding)})")
                
                # Save progress after each successful embedding
                with open("embedded_prisma_data.json", "w", encoding="utf-8") as f:
                    json.dump(existing_embeddings, f, indent=2)
            else:
                print(f"  ✗ Failed to generate embedding for chunk {i+1}")
        
        print(f"Successfully generated embeddings for {len(existing_embeddings)} chunks")
        print("Embedded data saved to 'embedded_prisma_data.json'")
        
        return existing_embeddings
        
    except Exception as error:
        print(f"Error generating embeddings: {error}")
        return []

if __name__ == "__main__":
    print("Generating embeddings for chunked medical data...")
    print(f"Using Sambanova API: {SAMBANOVA_BASE_URL}")
    print(f"Model: E5-Mistral-7B-Instruct")
    
    embedded_chunks = generate_embeddings_for_chunks()
    
    if embedded_chunks:
        print("Embedding generation completed successfully!")
    else:
        print("Failed to generate embeddings.")