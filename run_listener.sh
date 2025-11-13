#!/bin/bash
# Script to run the PostgreSQL listener for RAG system updates

echo "Starting PostgreSQL listener for RAG system updates..."
echo "Make sure you have set the DATABASE_URL environment variable"
echo "Press Ctrl+C to stop"

# Run the listener
python postgres_listener.py