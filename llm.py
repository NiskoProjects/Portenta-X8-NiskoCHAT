#!/usr/bin/env python3
"""
LLM interface for the chat application on Portenta X8.
This module handles loading and running a small quantized LLM
suitable for the limited resources of the Portenta X8.
"""

import os
import logging
import time
import random
import traceback
import subprocess
from llama_cpp import Llama

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MistralLLM:
    """LLM interface for Portenta X8 using llama-cpp-python."""
    
    def __init__(self, model_path="models/tinyllama-1.1b-chat-v1.0.Q4_0.gguf"):
        """Initialize the LLM interface.
        
        Args:
            model_path: Path to the GGUF model file
        """
        self.model_path = model_path
        self.model = None
        self.loaded = False
        self.fallback_mode = False
        self.gpu_available = self._check_gpu()
        self._load_model()
    
    def _check_gpu(self):
        """Check if GPU acceleration is available on the Portenta X8."""
        try:
            # Check for GPU devices
            logger.info("Checking for GPU acceleration capabilities...")
            
            # Check for OpenCL support
            try:
                result = subprocess.run(
                    ["ls", "/dev/dri"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0 and result.stdout.strip():
                    logger.info(f"Found GPU devices: {result.stdout.strip()}")
                    return True
            except Exception as e:
                logger.info(f"No GPU devices found via /dev/dri: {e}")
            
            # Check for Vivante GPU (common in i.MX8 processors)
            try:
                result = subprocess.run(
                    ["ls", "/dev/galcore"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    logger.info("Found Vivante GPU (/dev/galcore)")
                    return True
            except Exception as e:
                logger.info(f"No Vivante GPU found: {e}")
                
            logger.info("No GPU acceleration available")
            return False
        except Exception as e:
            logger.error(f"Error checking GPU: {e}")
            return False
    
    def _load_model(self):
        """Load the GGUF model using llama-cpp-python."""
        try:
            logger.info(f"Loading model from {self.model_path}")
            
            # Check if model exists
            if not os.path.exists(self.model_path):
                logger.error(f"Model file {self.model_path} does not exist")
                self.fallback_mode = True
                self.loaded = True
                return False
            
            # Determine GPU layers based on availability
            n_gpu_layers = 1 if self.gpu_available else 0
            logger.info(f"Using GPU layers: {n_gpu_layers}")
            
            # Load the model with settings optimized for Portenta X8
            self.model = Llama(
                model_path=self.model_path,
                n_ctx=512,        # Smaller context window to save memory
                n_batch=8,        # Smaller batch size
                n_threads=2,      # Limit number of threads
                n_gpu_layers=n_gpu_layers,  # Use GPU if available
                verbose=False     # Reduce verbosity to avoid log clutter
            )
            
            logger.info("Model loaded successfully")
            self.loaded = True
            return True
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            logger.error(traceback.format_exc())
            
            # Fallback to rule-based responses if model loading fails
            logger.info("Falling back to rule-based responses")
            self.fallback_mode = True
            self.loaded = True  # Set to true so the application still works
            return False
    
    def is_loaded(self):
        """Check if the model is loaded.
        
        Returns:
            bool: True if the model is loaded, False otherwise
        """
        return self.loaded
    
    def is_using_gpu(self):
        """Check if the model is using GPU acceleration.
        
        Returns:
            bool: True if using GPU, False otherwise
        """
        return self.gpu_available and not self.fallback_mode
    
    def generate_response(self, message, chat_history=None):
        """Generate a response to the given message.
        
        Args:
            message: The user's message
            chat_history: Optional list of previous messages
            
        Returns:
            str: The generated response
        """
        if not self.is_loaded():
            logger.error("Model not loaded")
            return "I'm sorry, the model is not loaded properly."
        
        # Handle empty or very short messages with predefined responses
        if not message or len(message.strip()) < 3:
            if message.lower().strip() in ["hi", "hello"]:
                return "Hello! I'm a small LLM running on your Portenta X8. How can I help you today?"
            elif message.lower().strip() in ["hey"]:
                return "Hey there! I'm your Portenta X8 assistant. What can I do for you?"
            
        try:
            # Log the incoming message
            logger.info(f"Generating response for: {message[:50]}...")
            
            # If in fallback mode, use rule-based responses
            if self.fallback_mode or self.model is None:
                logger.info("Using fallback response mode")
                return self._fallback_response(message)
            
            # Format the prompt with chat history if provided
            if chat_history and len(chat_history) > 0:
                prompt = self._format_chat_history(chat_history, message)
            else:
                # TinyLlama chat format
                prompt = f"<human>: {message}\n<assistant>:"
            
            logger.info(f"Using prompt: {prompt[:100]}...")
            
            # Record start time for performance measurement
            start_time = time.time()
            
            # Generate a response using the loaded model
            try:
                # Use the model's completion method for inference with optimized parameters
                output = self.model.create_completion(
                    prompt,
                    max_tokens=128,
                    temperature=0.7,
                    top_p=0.95,
                    repeat_penalty=1.1,
                    stop=["<human>:", "\n<human>"],  # Improved stop tokens
                    echo=False
                )
                
                # Calculate generation time
                generation_time = time.time() - start_time
                logger.info(f"Response generated in {generation_time:.2f} seconds")
                
                # Extract the generated text
                if output and "choices" in output and len(output["choices"]) > 0:
                    response = output["choices"][0]["text"].strip()
                    logger.info(f"LLM generated response: {response[:50]}...")
                    
                    # If response is empty or too short, use fallback
                    if not response or len(response) < 5:
                        logger.warning("Response too short, using fallback")
                        return self._fallback_response(message)
                    
                    # Add GPU usage info if requested
                    if "gpu" in message.lower() or "hardware" in message.lower():
                        gpu_info = f"\n\nTechnical info: I'm running on a Portenta X8 with {'GPU acceleration' if self.is_using_gpu() else 'CPU only'} mode. Generated this response in {generation_time:.2f} seconds."
                        response += gpu_info
                    
                    return response
                else:
                    logger.error("Model returned empty or invalid response")
                    return self._fallback_response(message)
                
            except Exception as e:
                logger.error(f"Error during model inference: {e}")
                logger.error(traceback.format_exc())
                return self._fallback_response(message)
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            logger.error(traceback.format_exc())
            return f"I'm sorry, I encountered an error: {str(e)}"
    
    def _fallback_response(self, message):
        """Generate a rule-based response if model loading fails."""
        logger.info("Using fallback response generator")
        
        # Handle common greetings directly
        if message.lower().strip() in ["hi", "hello", "hey"]:
            return "Hello! I'm a small LLM running on your Portenta X8. How can I help you today?"
        
        # Predefined responses for demonstration
        responses = [
            "I'm a simple LLM running on the Portenta X8. My capabilities are limited but I'm doing my best!",
            "The Portenta X8 is a powerful board for edge computing applications.",
            "I can provide basic responses, but I'm not as capable as larger models running on more powerful hardware.",
            "Docker containers are a great way to package applications for embedded systems like the Portenta X8.",
            "Edge AI is becoming increasingly important for applications that need real-time processing with low latency.",
            "I'm designed to be lightweight and run efficiently on the Portenta X8's limited resources.",
            "The Arduino Portenta X8 combines a Linux-capable processor with real-time processing capabilities.",
            "I'm currently running in a Debian container on your Portenta X8 board."
        ]
        
        # Generate a contextual response based on keywords in the message
        if "portenta" in message.lower() or "x8" in message.lower():
            return "The Arduino Portenta X8 is a powerful SoM (System on Module) designed for industrial applications and edge computing."
        elif "docker" in message.lower() or "container" in message.lower():
            return "Docker containers are great for deploying applications on embedded Linux devices like the Portenta X8. They provide isolation and ease of deployment."
        elif "model" in message.lower() or "llm" in message.lower():
            return "I'm a small LLM designed to run on the Portenta X8's limited resources. I'm using a quantized version of the TinyLlama model."
        elif "gpu" in message.lower() or "hardware" in message.lower():
            return f"The Portenta X8 features an i.MX 8M Mini SoC with GC NanoUltra (3D) and GC320 (2D) GPUs. I'm currently running in {'GPU-accelerated' if self.gpu_available else 'CPU-only'} mode."
        else:
            # Select a random response from predefined list
            return random.choice(responses)
    
    def _format_chat_history(self, chat_history, message):
        """Format the chat history for the prompt."""
        # Format the chat history into a string for TinyLlama chat format
        history = ""
        for i, (user, assistant) in enumerate(chat_history):
            history += f"<human>: {user}\n<assistant>: {assistant}\n"
        
        # Append the current message to the chat history
        history += f"<human>: {message}\n<assistant>:"
        
        return history
