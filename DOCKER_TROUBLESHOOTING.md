# Docker Network Troubleshooting

## Issue: Cannot Connect to Docker Registry

If you see errors like:
```
failed to resolve source metadata for docker.io/library/python:3.10-slim
dial tcp: lookup registry-1.docker.io: i/o timeout
```

## Quick Fixes

### 1. Check Internet Connection
```bash
ping -c 3 google.com
```

### 2. Restart Docker Daemon
```bash
sudo systemctl restart docker
# Or if using Docker Desktop, restart the application
```

### 3. Check DNS Resolution
```bash
# Test DNS
nslookup registry-1.docker.io

# If using systemd-resolved (common on Ubuntu)
sudo systemctl restart systemd-resolved
```

### 4. Configure Docker DNS (if needed)
Create/edit `/etc/docker/daemon.json`:
```json
{
  "dns": ["8.8.8.8", "8.8.4.4"]
}
```
Then restart Docker:
```bash
sudo systemctl restart docker
```

### 5. Use Alternative Registry Mirror (if available)
Some regions have Docker registry mirrors. Check with your network admin.

### 6. Check Firewall/Proxy
If behind a corporate firewall/proxy:
```bash
# Set proxy for Docker (if needed)
sudo mkdir -p /etc/systemd/system/docker.service.d
sudo nano /etc/systemd/system/docker.service.d/http-proxy.conf
```

Add:
```ini
[Service]
Environment="HTTP_PROXY=http://proxy.example.com:8080"
Environment="HTTPS_PROXY=http://proxy.example.com:8080"
```

Then:
```bash
sudo systemctl daemon-reload
sudo systemctl restart docker
```

## Workaround: Build Without Frontend

If network issues persist, you can run backend only:

```bash
# Build and run only backend
docker-compose up backend --build

# Or skip build if image exists
docker-compose up backend
```

## Alternative: Local Development

Skip Docker entirely for now:

```bash
# Backend
python -m uvicorn api_server:app --host 0.0.0.0 --port 8000

# Frontend (in another terminal)
cd frontend
npm install
npm run dev
```

## Verify Docker Network

```bash
# Check if Docker can reach internet
docker run --rm curlimages/curl:latest curl -I https://registry-1.docker.io

# Check Docker network
docker network ls
```

## Common Solutions Summary

1. **Restart Docker**: `sudo systemctl restart docker`
2. **Check DNS**: Use Google DNS (8.8.8.8) in Docker config
3. **Check Firewall**: Ensure Docker can access internet
4. **Use Local Dev**: Skip Docker if network issues persist
5. **Wait and Retry**: Sometimes registry is temporarily unavailable

