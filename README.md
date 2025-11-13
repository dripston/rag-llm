# Medical RAG API

A Retrieval-Augmented Generation (RAG) system for medical records with a REST API for deployment on Render.

## Features

- REST API for asking questions about medical records
- CORS support for localhost:3000 and localhost:3500
- Endpoint for updating RAG with new data
- Integration with Pinecone vector database
- Sambanova LLM for generating responses

## API Endpoints

### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "message": "Medical RAG API is running"
}
```

### `POST /ask`
Ask questions about medical records.

**Request:**
```json
{
  "question": "What are the diagnostic differentials for patient USR003?"
}
```

**Response:**
```json
{
  "question": "What are the diagnostic differentials for patient USR003?",
  "answer": "Based on the patient records, the potential diagnoses are..."
}
```

### `POST /update_rag`
Update RAG with new medical data.

**Request:**
```json
{
  "patient_id": "USR003",
  "data": "New medical information"
}
```

**Response:**
```json
{
  "message": "Data received for RAG update",
  "received_items": 1
}
```

## Deployment to Render

1. Fork this repository to your GitHub account
2. Create a new Web Service on Render
3. Connect it to your forked repository
4. Set the following environment variables in Render:
   - `PINECONE_API_KEY`
   - `LLM_API_KEY`
   - `SAMBANOVA_BASE_URL`
   - `DATABASE_URL`

The service will automatically deploy using the configuration in `render.yaml`.