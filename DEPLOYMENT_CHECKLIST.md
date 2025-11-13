# Deployment Checklist

## Pre-deployment

- [ ] Verify all environment variables are set:
  - `PINECONE_API_KEY`
  - `LLM_API_KEY`
  - `SAMBANOVA_BASE_URL`
  - `DATABASE_URL`
- [ ] Check that requirements.txt has correct package versions
- [ ] Verify render.yaml configuration
- [ ] Test local server with `python app.py`
- [ ] Run basic API tests with `python test_deployment.py`

## Render Deployment

- [ ] Fork repository to GitHub
- [ ] Create new Web Service on Render
- [ ] Connect to GitHub repository
- [ ] Set environment variables in Render dashboard
- [ ] Verify automatic deployment
- [ ] Check logs for any errors

## Post-deployment

- [ ] Test health endpoint: `GET /health`
- [ ] Test ask endpoint: `POST /ask`
- [ ] Test update RAG endpoint: `POST /update_rag`
- [ ] Verify CORS is working for localhost:3000 and localhost:3500
- [ ] Monitor logs for any runtime errors

## Troubleshooting

- If deployment fails due to package installation:
  - Check Python version compatibility
  - Verify package versions in requirements.txt
  - Consider using pre-compiled wheels with `--only-binary=all`
  
- If API endpoints fail:
  - Check environment variables are correctly set
  - Verify Pinecone API key and index configuration
  - Check Sambanova API key and endpoint
  - Review logs for specific error messages

## Monitoring

- [ ] Set up log monitoring
- [ ] Configure error alerts
- [ ] Monitor API response times
- [ ] Check for rate limiting issues