# Docker Setup Guide

This guide explains how to dockerize and run the Trading Analytics Platform.

## Prerequisites

- Docker installed ([Install Docker](https://docs.docker.com/get-docker/))
- Docker Compose installed (usually comes with Docker Desktop)
- Google Cloud credentials file (for BigQuery access)

## Quick Start

### 1. Get Google Cloud Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create or select a project
3. Enable BigQuery API
4. Create a Service Account:
   - Go to "IAM & Admin" > "Service Accounts"
   - Click "Create Service Account"
   - Grant "BigQuery Data Viewer" and "BigQuery Job User" roles
5. Create a JSON key:
   - Click on the service account
   - Go to "Keys" tab
   - Click "Add Key" > "Create new key" > "JSON"
   - Download the JSON file

### 2. Place Credentials File

Place the downloaded JSON file in the project root and rename it to `google_credentials.json`:

```bash
# Example location
/home/meid/Desktop/TechVision-deriv-hackathon/google_credentials.json
```

**⚠️ IMPORTANT:** This file is already in `.gitignore` - never commit it to Git!

### 3. Configure Environment (Optional)

Create a `.env` file in the project root (or use the example):

```bash
cp config/.env.example .env
```

Edit `.env` to set your preferences:

```env
# Set to false to use real BigQuery (requires credentials)
USE_MOCK_INTERNAL=true
USE_MOCK_EXTERNAL=true

# BigQuery settings (if using real BigQuery)
BIGQUERY_PROJECT=your-project-id
BIGQUERY_DATASET=your-dataset-name
```

### 4. Build and Run

```bash
# Build and start the container
docker-compose up --build

# Or run in detached mode (background)
docker-compose up -d --build
```

The API will be available at: `http://localhost:8000`

### 5. Test the API

```bash
# Health check
curl http://localhost:8000/health

# Dashboard load
curl -X POST http://localhost:8000/api/dashboard/load \
  -H "Content-Type: application/json" \
  -d '{}'

# Chat query
curl -X POST http://localhost:8000/api/chat/query \
  -H "Content-Type: application/json" \
  -d '{"user_query": "Why did we lose money today?"}'
```

## Docker Commands

### Build Only
```bash
docker-compose build
```

### Start Services
```bash
docker-compose up
```

### Stop Services
```bash
docker-compose down
```

### View Logs
```bash
# All services
docker-compose logs

# Backend only
docker-compose logs backend

# Follow logs (like tail -f)
docker-compose logs -f backend
```

### Execute Commands in Container
```bash
# Open a shell in the running container
docker-compose exec backend bash

# Run Python commands
docker-compose exec backend python main.py
```

### Rebuild After Code Changes
```bash
# Rebuild and restart
docker-compose up --build

# Or just restart (if no dependency changes)
docker-compose restart
```

## Development Workflow

### Option 1: Develop Locally, Dockerize for Demo

1. **During Development:**
   ```bash
   # Run locally (faster iteration)
   python main.py
   # or
   python -m uvicorn api_server:app --reload
   ```

2. **Before Demo:**
   ```bash
   # Test Docker build
   docker-compose up --build
   ```

### Option 2: Full Docker Development

1. **Mount source code as volume** (edit `docker-compose.yml`):
   ```yaml
   volumes:
     - ./google_credentials.json:/app/google_credentials.json:ro
     - ./config:/app/config:ro
     - ./src:/app/src:ro  # Add this for live code updates
   ```

2. **Use volume mounts for hot-reload** (requires uvicorn reload mode)

## Troubleshooting

### Issue: "Cannot find google_credentials.json"

**Solution:** Make sure the file exists in the project root:
```bash
ls -la google_credentials.json
```

If it doesn't exist, download it from Google Cloud Console.

### Issue: "Permission denied" on credentials file

**Solution:** Fix file permissions:
```bash
chmod 644 google_credentials.json
```

### Issue: BigQuery connection fails

**Solutions:**
1. Verify credentials file is correct
2. Check environment variables in `.env`
3. Ensure BigQuery API is enabled in Google Cloud
4. Verify service account has correct permissions

### Issue: Port 8000 already in use

**Solution:** Change the port in `docker-compose.yml`:
```yaml
ports:
  - "8001:8000"  # Use port 8001 on host
```

### Issue: Container keeps restarting

**Solution:** Check logs:
```bash
docker-compose logs backend
```

Common causes:
- Missing credentials file
- Import errors
- Port conflicts

## Production Considerations

For production deployment:

1. **Security:**
   - Use Docker secrets or environment variables for credentials
   - Don't mount credential files directly
   - Use specific CORS origins instead of `*`

2. **Performance:**
   - Use multi-stage builds to reduce image size
   - Add resource limits in `docker-compose.yml`
   - Use production WSGI server (gunicorn with uvicorn workers)

3. **Monitoring:**
   - Add health checks (already included)
   - Set up logging aggregation
   - Monitor container resources

## Architecture Notes

- **BigQuery is NOT in Docker** - it's a cloud service
- **Credentials are mounted** - the JSON file is read-only mounted into the container
- **Networking** - services communicate via Docker network (`trading-network`)
- **Frontend** - commented out in `docker-compose.yml`, uncomment when ready

## API Endpoints

Once running, the API provides:

- `GET /` - API information
- `GET /health` - Health check
- `POST /api/dashboard/load` - Fast dashboard load
- `POST /api/chat/query` - Chat query with full analysis

See `api_server.py` for full API documentation.

