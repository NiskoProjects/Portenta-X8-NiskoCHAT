# Portenta X8 LLM Chat Server Deployment Guide

This guide provides step-by-step instructions for deploying the TinyLlama LLM chat server on your Arduino Portenta X8 board using Docker.

## Prerequisites

- Arduino Portenta X8 board with the latest firmware (see `portenta_x8_flashing_guide.md`)
- Docker installed on the Portenta X8
- Network connectivity for the board
- At least 2GB of free storage space
- SSH access to the Portenta X8

## Step 1: Set Up Your Portenta X8

1. Ensure your Portenta X8 is properly flashed with the latest firmware
2. Connect the board to your network via Ethernet or Wi-Fi
3. Determine the IP address of your board (check your router or use `ip addr` command)
4. SSH into your Portenta X8:
   ```
   ssh user@<board-ip-address>
   ```

## Step 2: Install Docker (if not already installed)

The Portenta X8 typically comes with Docker pre-installed. If not, you can install it with:

```bash
sudo apt-get update
sudo apt-get install -y docker.io
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker $USER
```

Log out and log back in for the group changes to take effect.

## Step 3: Clone the Repository

Clone this repository to your Portenta X8:

```bash
git clone <repository-url> portenta-llm-chat
cd portenta-llm-chat
```

Alternatively, you can copy the files to the board using SCP:

```bash
scp -r /path/to/local/project user@<board-ip-address>:~/portenta-llm-chat
```

## Step 4: Build the Docker Image

Build the Docker image on the Portenta X8:

```bash
cd portenta-llm-chat
docker build -t portenta-llm-chat .
```

Note: This will take some time as it downloads the model.

## Step 5: Run the Docker Container with GPU Acceleration

Start the container with GPU acceleration:

```bash
docker run -d --name llm-chat -p 8080:8080 --device /dev/dri:/dev/dri --device /dev/galcore:/dev/galcore portenta-llm-chat
```

This will:
- Run the container in detached mode (`-d`)
- Name the container "llm-chat"
- Map port 8080 on the host to port 8080 in the container
- Pass through GPU devices to enable acceleration

## Step 6: Access the Chat Interface

Open a web browser and navigate to:

```
http://<board-ip-address>:8080
```

You should see the chat interface and be able to interact with the TinyLlama LLM.

## Step 7: Configure Auto-start on Boot (Optional)

To configure the LLM chat server to start automatically when the Portenta X8 boots, follow the instructions in the [Auto-start Guide](./autostart_guide.md).

## Troubleshooting

### Container Won't Start

Check the container logs:

```bash
docker logs llm-chat
```

### Not Enough Memory

If the container fails due to memory constraints, you can limit the memory usage:

```bash
docker run -d --name llm-chat -p 8080:8080 --memory=1g --memory-swap=1g --device /dev/dri:/dev/dri --device /dev/galcore:/dev/galcore portenta-llm-chat
```

### Model Download Issues

If you have issues downloading the model, you can pre-download it on a more powerful machine and copy it to the Portenta X8:

1. Run the `download_model.py` script on your development machine
2. Copy the `models` directory to the Portenta X8
3. Build the Docker image with the pre-downloaded model

### GPU Acceleration Not Working

If GPU acceleration isn't working:

1. Check if the GPU devices are properly detected:
   ```bash
   ls /dev/dri
   ls /dev/galcore
   ```

2. Ensure the Docker container has access to the GPU devices:
   ```bash
   docker exec -it llm-chat ls -la /dev/dri
   docker exec -it llm-chat ls -la /dev/galcore
   ```

3. Check the application logs for GPU detection messages:
   ```bash
   docker logs llm-chat | grep -i gpu
   ```

### Web Interface Not Accessible

Check that:
- The container is running: `docker ps`
- The port is correctly mapped: `docker port llm-chat`
- No firewall is blocking the connection

## Managing the Container

### Stop the Container

```bash
docker stop llm-chat
```

### Start the Container

```bash
docker start llm-chat
```

### Remove the Container

```bash
docker stop llm-chat
docker rm llm-chat
```

### View Container Logs

```bash
docker logs llm-chat
```

## Performance Considerations

The Portenta X8 has limited resources compared to a desktop computer. To optimize performance:

1. The TinyLlama model is quantized to 4-bit precision to reduce memory usage
2. GPU acceleration is enabled to improve inference speed
3. The response timeout is set to 5 minutes to allow for longer processing times
4. Special handling for simple messages like "hi" provides immediate responses

## Security Considerations

This deployment is intended for development and testing purposes. For production use:

1. Enable HTTPS by setting up a reverse proxy with SSL/TLS
2. Implement proper authentication
3. Restrict network access to the server
4. Keep the Portenta X8 firmware and Docker updated with security patches
