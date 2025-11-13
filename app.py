import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from medical_rag import MedicalRAG

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure CORS for localhost:3000 and localhost:3500
CORS(app, origins=["http://localhost:3000", "http://localhost:3500"])

# Initialize the Medical RAG system
rag = MedicalRAG()

@app.route('/', methods=['GET'])
def home():
    """Root endpoint"""
    return jsonify({"message": "Medical RAG API is running", "endpoints": ["/health", "/ask", "/update_rag"]}), 200

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Medical RAG API is running"}), 200

@app.route('/ask', methods=['POST'])
def ask_question():
    """Endpoint to ask questions about medical records"""
    try:
        data = request.get_json()
        
        if not data or 'question' not in data:
            return jsonify({"error": "Missing 'question' in request body"}), 400
        
        question = data['question']
        response = rag.ask_question(question)
        
        return jsonify({"question": question, "answer": response}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/update_rag', methods=['POST'])
def update_rag_data():
    """Endpoint to update RAG with new data"""
    try:
        # In a real implementation, this would:
        # 1. Receive new data from the client
        # 2. Process the data through chunking
        # 3. Generate embeddings
        # 4. Store in Pinecone
        
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # For now, we'll just acknowledge the request
        # In a full implementation, this would process the new data
        print(f"Received data for RAG update: {data}")
        
        # TODO: Implement actual RAG update logic here
        # This would involve:
        # 1. Chunking the new data
        # 2. Generating embeddings
        # 3. Storing in Pinecone
        
        return jsonify({
            "message": "Data received for RAG update", 
            "received_items": len(data) if isinstance(data, list) else 1
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)