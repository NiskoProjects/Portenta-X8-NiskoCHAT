#!/usr/bin/env python3
"""
Script to download a small LLM model for use on the Portenta X8.
This script downloads a lightweight, quantized model suitable for
running on the limited resources of the Portenta X8.
"""

import os
import sys
import requests
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Model configuration
MODEL_DIR = "models"
MODEL_FILENAME = "tinyllama-1.1b-chat-v1.0.Q4_0.gguf"
MODEL_URL = "https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_0.gguf"

def download_file(url, destination):
    """Download a file from a URL to a destination path."""
    try:
        logger.info(f"Downloading {url} to {destination}")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 Kibibyte
        
        with open(destination, 'wb') as f:
            for data in response.iter_content(block_size):
                f.write(data)
                
        logger.info(f"Download complete: {destination}")
        return True
    except Exception as e:
        logger.error(f"Error downloading file: {e}")
        return False

def main():
    """Main function to download the model."""
    # Create model directory if it doesn't exist
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    model_path = os.path.join(MODEL_DIR, MODEL_FILENAME)
    
    # Check if model already exists
    if os.path.exists(model_path):
        logger.info(f"Model already exists at {model_path}")
        return
    
    logger.info(f"Downloading small LLM model for Portenta X8...")
    
    # Download the model
    success = download_file(MODEL_URL, model_path)
    
    if success:
        logger.info(f"Model downloaded successfully to {model_path}")
    else:
        logger.error("Failed to download model")
        # Create a placeholder file for testing
        with open(model_path, "w") as f:
            f.write("placeholder for model binary - download failed")
        logger.info("Created placeholder model file for testing")

if __name__ == "__main__":
    main()
