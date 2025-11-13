"""
Test script to verify that all required packages can be imported
"""

try:
    import os
    print("✓ os imported successfully")
except ImportError as e:
    print(f"✗ Failed to import os: {e}")

try:
    import json
    print("✓ json imported successfully")
except ImportError as e:
    print(f"✗ Failed to import json: {e}")

try:
    from flask import Flask, request, jsonify
    print("✓ flask imported successfully")
except ImportError as e:
    print(f"✗ Failed to import flask: {e}")

try:
    from flask_cors import CORS
    print("✓ flask_cors imported successfully")
except ImportError as e:
    print(f"✗ Failed to import flask_cors: {e}")

try:
    from dotenv import load_dotenv
    print("✓ python-dotenv imported successfully")
except ImportError as e:
    print(f"✗ Failed to import python-dotenv: {e}")

try:
    from pinecone import Pinecone
    print("✓ pinecone-client imported successfully")
except ImportError as e:
    print(f"✗ Failed to import pinecone-client: {e}")

try:
    import requests
    print("✓ requests imported successfully")
except ImportError as e:
    print(f"✗ Failed to import requests: {e}")

try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    print("✓ langchain.text_splitter imported successfully")
except ImportError as e:
    print(f"✗ Failed to import langchain.text_splitter: {e}")

try:
    from langchain.docstore.document import Document
    print("✓ langchain.docstore.document imported successfully")
except ImportError as e:
    print(f"✗ Failed to import langchain.docstore.document: {e}")

try:
    import numpy as np
    print("✓ numpy imported successfully")
except ImportError as e:
    print(f"✗ Failed to import numpy: {e}")

print("\nTest completed!")