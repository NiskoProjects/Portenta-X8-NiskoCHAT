#!/usr/bin/env python3
"""
Flask web server for the LLM chat interface.
This application provides a web-based chat interface to interact with
the quantized LLM running on the Portenta X8.
"""

import os
import logging
import time
import threading
from flask import Flask, render_template, request, jsonify
from llm import TinyLlamaLLM

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Initialize the LLM
model = TinyLlamaLLM()

class ResponseGenerator:
    """Helper class to generate responses with timeout."""
    
    def __init__(self, model):
        self.model = model
        self.response = None
        self.error = None
    
    def generate(self, message, chat_history):
        """Generate a response with the model."""
        try:
            self.response = self.model.generate_response(message, chat_history)
        except Exception as e:
            self.error = str(e)
            logger.error(f"Error in response generation thread: {e}")

@app.route('/')
def index():
    """Render the main chat interface."""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """API endpoint to process chat messages and get responses from the LLM."""
    try:
        data = request.json
        message = data.get('message', '')
        chat_history = data.get('history', [])
        
        # Log the incoming message
        logger.info(f"Received message: {message}")
        
        # For very short messages, use direct responses
        if len(message.strip()) < 3:
            if message.lower().strip() in ["hi", "hello", "hey"]:
                return jsonify({
                    'response': "Hello! I'm a small LLM running on your Portenta X8. How can I help you today?",
                    'status': 'success'
                })
        
        # Generate response with timeout
        generator = ResponseGenerator(model)
        thread = threading.Thread(target=generator.generate, args=(message, chat_history))
        thread.start()
        
        # Wait for response with timeout (5 minutes = 300 seconds)
        timeout = 300  # seconds
        start_time = time.time()
        thread.join(timeout)
        
        # Check if response was generated within timeout
        if thread.is_alive():
            logger.warning(f"Response generation timed out after {timeout} seconds")
            return jsonify({
                'response': "I'm sorry, it's taking me longer than expected to generate a response. The Portenta X8 has limited resources, so complex queries might take time to process.",
                'status': 'timeout'
            })
        
        # Check for errors
        if generator.error:
            logger.error(f"Error generating response: {generator.error}")
            return jsonify({
                'response': "I'm sorry, I encountered an error processing your request.",
                'status': 'error',
                'error': generator.error
            }), 500
        
        # Return the generated response
        return jsonify({
            'response': generator.response,
            'status': 'success'
        })
    
    except Exception as e:
        logger.error(f"Error processing chat request: {e}")
        return jsonify({
            'response': "I'm sorry, I encountered an error processing your request.",
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint to verify the server is running."""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model.is_loaded(),
        'gpu_enabled': hasattr(model, 'is_using_gpu') and model.is_using_gpu(),
        'model_type': 'TinyLlama-1.1B-Chat'
    })

if __name__ == '__main__':
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 8080))
    
    # Run the Flask app
    logger.info(f"Starting server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
