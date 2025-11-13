import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from medical_rag import MedicalRAG
from background_processor import start_background_processor, queue_file_for_processing

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure CORS for localhost:3000 and localhost:3500
CORS(app, origins=["http://localhost:3000", "http://localhost:3500"])

# Initialize the Medical RAG system
rag = MedicalRAG()

# Start background processor
start_background_processor()

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
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Log the received data
        print(f"Received data for RAG update: {data}")
        
        # Extract the actual data from the payload
        payload_data = data.get('data', data)
        
        # Save received data to a temporary file for processing
        import json
        import os
        from datetime import datetime
        
        # Create a timestamp for this update
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        temp_file = f"temp_update_{timestamp}.json"
        
        # Save the received data
        with open(temp_file, "w") as f:
            json.dump(payload_data, f, indent=2, default=str)
        
        print(f"Data saved to {temp_file}")
        
        # Queue the file for background processing
        queue_file_for_processing(temp_file)
        print("Queued RAG update for background processing")
        
        return jsonify({
            "message": "Data received and queued for RAG update", 
            "received_items": len(payload_data) if isinstance(payload_data, list) else 1,
            "timestamp": timestamp
        }), 200
        
    except Exception as e:
        print(f"Error in update_rag_data: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)