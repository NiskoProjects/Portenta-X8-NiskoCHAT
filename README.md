# Portenta X8 NiskoChat

A lightweight, GPU-accelerated TinyLlama LLM chat server running on the Arduino Portenta X8 board using Docker.

![Portenta X8 LLM](https://docs.arduino.cc/static/8e52abe5c2c7a94ea8c7b476c8c8c7a7/2f0d5/portenta-x8-angle.webp)

## Overview

This project implements a web-based chat interface powered by a quantized TinyLlama LLM running on the Arduino Portenta X8 board. The system leverages Docker for containerization and the Portenta X8's GPU for acceleration.

### Features

- **Lightweight LLM**: Uses TinyLlama (1.1B parameters), quantized to 4-bit precision for efficient inference
- **GPU Acceleration**: Leverages the Portenta X8's GPU capabilities for faster inference
- **Web Interface**: Clean, responsive chat interface accessible from any device
- **Auto-start on Boot**: Configured to automatically start when the Portenta X8 boots
- **Containerized**: Packaged in a Docker container for easy deployment and isolation

## Getting Started

### Prerequisites

- Arduino Portenta X8 board with the latest firmware
- Docker installed on the Portenta X8
- Network connectivity for the Portenta X8
- At least 2GB of free storage space

### Installation

1. Clone this repository to your Portenta X8:

```bash
git clone https://github.com/yourusername/Portenta-X8-NiskoChat.git
cd Portenta-X8-NiskoChat
```

2. Build the Docker image:

```bash
docker build -t portenta-llm-chat .
```

3. Run the container:

```bash
docker run -d --name llm-chat -p 8080:8080 --device /dev/dri:/dev/dri --device /dev/galcore:/dev/galcore portenta-llm-chat
```

4. Access the chat interface:

```
http://<portenta-x8-ip-address>:8080
```

### Auto-start Setup

To configure the NiskoChat server to start automatically on boot, follow the instructions in the [Auto-start Guide](./docs/autostart_guide.md).

## Project Structure

- `app.py`: Flask web server for the chat interface
- `llm.py`: Interface to the TinyLlama LLM
- `download_model.py`: Script to download and prepare the quantized model
- `Dockerfile`: Defines the Debian-based container with all dependencies
- `requirements.txt`: Python dependencies
- `templates/`: HTML templates for the web interface
- `static/`: CSS and JavaScript files for the web interface
- `docs/`: Documentation and guides

## Documentation

- [Portenta X8 Flashing Guide](./docs/portenta_x8_flashing_guide.md): Instructions for flashing your Portenta X8 board
- [Deployment Guide](./docs/deployment_guide.md): Detailed deployment instructions
- [Auto-start Guide](./docs/autostart_guide.md): Guide for configuring auto-start on boot
- [GPU Acceleration Guide](./docs/gpu_acceleration_guide.md): Details on GPU acceleration for LLM inference

## Performance

The TinyLlama model is optimized for the limited resources of the Portenta X8:
- Model size: ~500MB (4-bit quantized)
- RAM usage: ~800MB
- Inference time: 1-5 seconds per response (with GPU acceleration)

## Limitations

- The TinyLlama model is significantly smaller than models like GPT-4 or Claude, so responses may be less sophisticated
- The Portenta X8 has limited RAM and processing power, which may affect performance with complex queries
- GPU acceleration is limited by the capabilities of the Portenta X8's GPU

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [TinyLlama](https://github.com/jzhang38/TinyLlama) for the base model
- [llama-cpp-python](https://github.com/abetlen/llama-cpp-python) for the Python bindings
- [Arduino](https://www.arduino.cc/) for the Portenta X8 platform
