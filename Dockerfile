FROM debian:bullseye-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create model directory
RUN python3 download_model.py

# Expose the port for the web server
EXPOSE 8080

# Command to run the application
CMD ["python3", "app.py"]
