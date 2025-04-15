# Portenta X8 LLM Chat Server Auto-Start Guide

This guide explains how to manage the LLM Chat Server that has been configured to automatically start on boot on your Arduino Portenta X8.

## How It Works

The system uses two systemd services to manage the LLM Chat Server:

1. **prepare-llm-chat.service**: Ensures the Docker image exists before starting the main service
2. **llm-chat.service**: Starts the Docker container with the LLM Chat Server

These services are configured to start automatically when your Portenta X8 boots up.

## Managing the Services

### Checking Service Status

To check the status of the services:

```bash
sudo systemctl status prepare-llm-chat.service
sudo systemctl status llm-chat.service
```

### Starting the Services Manually

If the services are not running, you can start them manually:

```bash
sudo systemctl start prepare-llm-chat.service
sudo systemctl start llm-chat.service
```

### Stopping the Services

To stop the LLM Chat Server:

```bash
sudo systemctl stop llm-chat.service
```

### Disabling Auto-Start

If you want to disable the auto-start feature:

```bash
sudo systemctl disable prepare-llm-chat.service
sudo systemctl disable llm-chat.service
```

### Re-enabling Auto-Start

To re-enable the auto-start feature:

```bash
sudo systemctl enable prepare-llm-chat.service
sudo systemctl enable llm-chat.service
```

## Service Logs

To view the logs for the services:

```bash
sudo journalctl -u prepare-llm-chat.service
sudo journalctl -u llm-chat.service
```

To follow the logs in real-time:

```bash
sudo journalctl -u llm-chat.service -f
```

## Docker Container Logs

To view the logs from the Docker container:

```bash
sudo docker logs llm-chat
```

To follow the Docker logs in real-time:

```bash
sudo docker logs -f llm-chat
```

## Troubleshooting

If the service fails to start:

1. Check the service logs for errors:
   ```bash
   sudo journalctl -u prepare-llm-chat.service
   sudo journalctl -u llm-chat.service
   ```

2. Ensure Docker is running:
   ```bash
   sudo systemctl status docker
   ```

3. Verify the Docker image exists:
   ```bash
   sudo docker images | grep portenta-llm-chat
   ```

4. Check if the container is already running:
   ```bash
   sudo docker ps | grep llm-chat
   ```

5. Manually build the Docker image:
   ```bash
   cd /home/fio/portenta-llm-chat
   sudo docker build -t portenta-llm-chat .
   ```

## Service Configuration Files

The service configuration files are located at:

- `/etc/systemd/system/prepare-llm-chat.service`
- `/etc/systemd/system/llm-chat.service`

If you need to modify these files, edit them with a text editor and then reload the systemd daemon:

```bash
sudo nano /etc/systemd/system/llm-chat.service
sudo systemctl daemon-reload
```

## Accessing the LLM Chat Server

Once the service is running, you can access the LLM Chat Server at:

```
http://<portenta-x8-ip-address>:8080
```
