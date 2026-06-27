# 📱 WhatsApp Gateway

A lightweight, high-performance standalone WhatsApp Gateway built with **Node.js** and **Baileys**. Perfect for sending notifications (text, images, videos) and controlling integrations via WhatsApp. It can be run either as a standalone Docker container or as the backend for the official Home Assistant Integration.

[![GitHub Release](https://img.shields.io/github/v/release/FaserF/WhatsappGateway?style=flat-square)](https://github.com/FaserF/WhatsappGateway/releases)
[![Docker Image](https://img.shields.io/badge/docker-image-blue.svg?logo=docker&style=flat-square)](https://github.com/users/FaserF/packages/container/package/whatsappgateway)
[![CI Status](https://img.shields.io/github/actions/workflow/status/FaserF/WhatsappGateway/ci.yml?branch=main&style=flat-square)](https://github.com/FaserF/WhatsappGateway/actions)
[![License](https://img.shields.io/github/license/FaserF/WhatsappGateway?style=flat-square)](LICENSE)

---

## 🚀 Features

- **Decoupled Standalone Run**: Run anywhere Docker is supported (Linux, macOS, Windows).
- **Multi-Platform Support**: Ready for `amd64` and `arm64` architectures.
- **REST API**: Simple endpoints for sending messages, media, and managing sessions.
- **Webhook Integration**: Receive events like incoming messages, status updates, and session states.
- **Web UI & QR Code pairing**: Scan a QR code or pair via phone number.
- **Low Footprint**: Lightweight Docker image built on Alpine.

---

## 🛠️ Standalone Installation

### Option 1: Docker Compose (Recommended)

Create a `docker-compose.yml` file:

```yaml
services:
  whatsapp-gateway:
    image: ghcr.io/faserf/whatsappgateway:latest
    container_name: whatsapp-gateway
    restart: unless-stopped
    ports:
      - "8066:8066"
    volumes:
      - ./data:/data
      - ./media:/media
    environment:
      - PORT=8066
      - DATA_DIR=/data
      - MEDIA_FOLDER=/media
      - LOG_LEVEL=info
      # - API_TOKEN=your_secure_token_here
```

Run with:

```bash
docker compose up -d
```

### Option 2: Docker CLI

```bash
docker run -d \
  --name whatsapp-gateway \
  --restart unless-stopped \
  -p 8066:8066 \
  -v ./data:/data \
  -v ./media:/media \
  -e PORT=8066 \
  ghcr.io/faserf/whatsappgateway:latest
```

---

## ⚙️ Configuration & Environment Variables

Configure the gateway using environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Listening port for the API and Web UI. | `8066` |
| `DATA_DIR` | Storage directory for authentication files and persistent tokens. | `/data` |
| `MEDIA_FOLDER` | Directory where incoming/outgoing media streams are handled. | `/media` |
| `API_TOKEN` | Secret key for securing API endpoints. If omitted, one is auto-generated. | *Auto-generated* |
| `ADMIN_NUMBERS` | Comma-separated list of WhatsApp numbers allowed to use admin commands. | `""` |
| `LOG_LEVEL` | Logging level (`trace`, `debug`, `info`, `warn`, `error`, `fatal`). | `info` |
| `WEBHOOK_ENABLED` | Enable forwarding incoming events/messages to a URL. | `false` |
| `WEBHOOK_URL` | Destination URL for webhook payloads. | `""` |
| `WEBHOOK_TOKEN` | Bearer token sent in webhook headers. | `""` |
| `UI_AUTH_ENABLED` | Secure the pairing web UI with a password. | `false` |
| `UI_AUTH_PASSWORD` | Password for the pairing web UI. | `""` |
| `MARK_ONLINE` | Keep WhatsApp status as "Online" continuously. | `false` |
| `RESET_SESSION` | Wipes the current authentication cache directory on startup. | `false` |
| `WELCOME_MESSAGE_ENABLED` | Send welcome role message to new contacts on first DM. | `true` |
| `ADMIN_NOTIFICATIONS_ENABLED` | Send status/pairing notifications to admin numbers. | `true` |
| `SEND_MESSAGE_TIMEOUT` | Timeout in ms for sending WhatsApp messages. | `25000` |
| `KEEP_ALIVE_INTERVAL` | Keepalive interval in ms for WhatsApp connection. | `30000` |
| `MASK_SENSITIVE_DATA` | Masks contact phone numbers in logs. | `false` |
| `MESSAGE_SEND_INTERVAL` | Interval delay in ms between consecutive messages. | `1000` |
| `GROUP_FETCH_INTERVAL` | Interval in ms for background syncing of chat groups. | `300000` |
| `GROUP_FETCH_COOLDOWN_ON_ERROR` | Backoff delay on sync error. | `60000` |
| `GROUP_FETCH_COOLDOWN_ON_RATE_LIMIT` | Backoff delay on rate-limits. | `900000` |
| `NODE_TLS_REJECT_UNAUTHORIZED` | Rejects unauthorized SSL certificates (`1` to enable, `0` to disable). | `1` |

---

## 📚 API Documentation

See [API.md](API.md) for detailed descriptions of REST API endpoints.

---

## 👨‍💻 License

This project is open-source under the [MIT License](LICENSE).
