try:
    import pinecone
    print("Pinecone imported successfully")
    print("Pinecone module attributes:", [attr for attr in dir(pinecone) if not attr.startswith('_')])
except Exception as e:
    print(f"Error importing pinecone: {e}")

try:
    # Try to initialize the Pinecone client
    client = pinecone.Pinecone(api_key="test-key")
    print("Pinecone client initialized successfully")
except Exception as e:
    print(f"Error initializing Pinecone client: {e}")