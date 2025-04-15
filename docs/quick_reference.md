# Portenta X8 LLM Chat Server - Quick Reference

This quick reference guide provides essential commands and information for working with the Portenta X8 LLM Chat Server.

## Docker Commands

### Build the Docker image
```bash
docker build -t portenta-llm-chat .
```

### Run the container with GPU acceleration
```bash
docker run -d --name llm-chat -p 8080:8080 --device /dev/dri:/dev/dri --device /dev/galcore:/dev/galcore portenta-llm-chat
```

### View container logs
```bash
docker logs llm-chat
```

### Stop and remove the container
```bash
docker stop llm-chat
docker rm llm-chat
```

## Auto-start Management

### Check service status
```bash
sudo systemctl status llm-chat.service
```

### Start/stop service
```bash
sudo systemctl start llm-chat.service
sudo systemctl stop llm-chat.service
```

### Enable/disable auto-start
```bash
sudo systemctl enable llm-chat.service
sudo systemctl disable llm-chat.service
```

## Model Information

- **Model**: TinyLlama (1.1B parameters)
- **Quantization**: 4-bit
- **Context Window**: 512 tokens
- **Batch Size**: 8
- **Threads**: 2
- **GPU Layers**: 1 (when GPU is available)

## Web Interface

- **URL**: http://<portenta-x8-ip-address>:8080
- **API Endpoint**: http://<portenta-x8-ip-address>:8080/api/chat
- **Health Check**: http://<portenta-x8-ip-address>:8080/api/health

## Performance Expectations

- **Response Time**: 1-5 seconds (with GPU acceleration)
- **Memory Usage**: ~800MB
- **Timeout**: 5 minutes (300 seconds)

## File Locations

- **Model File**: `/home/fio/portenta-llm-chat/models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf`
- **Application Code**: `/home/fio/portenta-llm-chat/`
- **Service Files**: `/etc/systemd/system/llm-chat.service` and `/etc/systemd/system/prepare-llm-chat.service`

## Troubleshooting Tips

1. **Container fails to start**: Check logs with `docker logs llm-chat`
2. **Model not found**: Run `download_model.py` script manually
3. **GPU not detected**: Verify device access with `ls /dev/dri` and `ls /dev/galcore`
4. **Slow responses**: Check system load with `top` and ensure GPU acceleration is enabled
5. **Service won't start**: Check systemd logs with `journalctl -u llm-chat.service`
