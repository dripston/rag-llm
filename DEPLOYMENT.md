# Deployment Guide for Medical RAG API

## Deploying to Render

1. Fork this repository to your GitHub account
2. Create a new Web Service on Render
3. Connect it to your forked repository
4. Set the following environment variables in Render:
   - `PINECONE_API_KEY` - Your Pinecone API key
   - `LLM_API_KEY` - Your Sambanova API key
   - `SAMBANOVA_BASE_URL` - Sambanova API base URL (default: https://api.sambanova.ai/v1)
   - `DATABASE_URL` - Your Prisma database connection URL

The service will automatically deploy using the configuration in `render.yaml`.

## Environment Variables

The following environment variables are required for the application to work:

| Variable | Description | Required |
|----------|-------------|----------|
| `PINECONE_API_KEY` | Pinecone API key for vector database access | Yes |
| `LLM_API_KEY` | Sambanova API key for embeddings and LLM | Yes |
| `SAMBANOVA_BASE_URL` | Sambanova API base URL | Optional (defaults to https://api.sambanova.ai/v1) |
| `DATABASE_URL` | Prisma database connection URL | Yes |
| `PORT` | Port for the web server (set by Render) | No (Render sets automatically) |

## API Endpoints

### Health Check
```
GET /health
```

### Ask Medical Questions
```
POST /ask
Content-Type: application/json

{
  "question": "What are the diagnostic differentials for patient USR003?"
}
```

### Update RAG with New Data
```
POST /update_rag
Content-Type: application/json

{
  "patient_id": "USR003",
  "data": "New medical information"
}
```

## CORS Configuration

The API is configured to accept requests from:
- http://localhost:3000
- http://localhost:3500

## Local Development

To run the API locally:

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set environment variables in a `.env` file:
   ```
   PINECONE_API_KEY=your_pinecone_key
   LLM_API_KEY=your_sambanova_key
   DATABASE_URL=your_database_url
   ```

3. Run the server:
   ```
   python app.py
   ```

The API will be available at http://localhost:8000