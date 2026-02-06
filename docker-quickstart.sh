#!/bin/bash
# Quick start script for Docker setup

set -e

echo "🚀 Trading Analytics Platform - Docker Quick Start"
echo "=================================================="
echo ""

# Check if credentials file exists
if [ ! -f "google_credentials.json" ]; then
    echo "⚠️  WARNING: google_credentials.json not found!"
    echo ""
    echo "To use real BigQuery, you need to:"
    echo "1. Download service account key from Google Cloud Console"
    echo "2. Place it in project root as 'google_credentials.json'"
    echo ""
    echo "For now, running in MOCK mode (no credentials needed)"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop."
    exit 1
fi

echo "✅ Docker is running"
echo ""

# Build and start
echo "📦 Building Docker image..."
docker-compose build

echo ""
echo "🚀 Starting services..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be healthy..."
sleep 5

# Check health
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is healthy!"
else
    echo "⚠️  Backend might still be starting. Check logs with: docker-compose logs backend"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "API Endpoints:"
echo "  - Health: http://localhost:8000/health"
echo "  - API Docs: http://localhost:8000/docs"
echo "  - Dashboard: POST http://localhost:8000/api/dashboard/load"
echo "  - Chat: POST http://localhost:8000/api/chat/query"
echo ""
echo "Useful commands:"
echo "  - View logs: docker-compose logs -f backend"
echo "  - Stop: docker-compose down"
echo "  - Restart: docker-compose restart"
echo ""