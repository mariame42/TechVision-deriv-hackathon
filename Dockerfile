# Trading Analytics Platform - Backend Dockerfile
# Uses Python 3.10 to match project requirements

FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
# build-essential needed for some Python packages that compile C extensions
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (Docker layer caching optimization)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Create a non-root user for security
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose the API port (FastAPI/uvicorn default)
EXPOSE 8000

# Health check to ensure container is running
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Command to run the application
# Using uvicorn for production-ready ASGI server
CMD ["python", "-m", "uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]

