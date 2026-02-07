# Trading Analytics Platform

A sophisticated AI-driven analytics platform for trading companies, built with LangGraph and LangChain.

## Architecture

This platform differentiates between two primary workflows:

1. **Dashboard Load (Fast Path)**: High-speed SQL-only path to load static overview cards
2. **Chat Query (Smart Path)**: Deep-reasoning path involving SQL, External APIs, Math Engines, and LLM analysis

## Tech Stack

- **Orchestration**: LangGraph
- **Tools**: LangChain
- **Language**: Python 3.10+
- **Data Source**: PostgreSQL (primary), BigQuery (legacy/mock), External Market APIs (legacy)

## Project Structure

See [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md) for detailed documentation.

## Quick Start

### Option A: Docker (Recommended for Hackathon/Demo)

**Fastest way to get started with a production-like setup:**

1. **Get Google Cloud Credentials:**
   - Download your service account JSON key from Google Cloud Console
   - Place it in project root as `google_credentials.json`

2. **Run with Docker:**
   ```bash
   docker-compose up --build
   ```

3. **Access the API:**
   - API: http://localhost:8000
   - Health check: http://localhost:8000/health

**Note:** Docker uses host network mode to connect to PostgreSQL on the host machine. Ensure PostgreSQL is running and accessible on `localhost:5432`.

### Option B: Local Development

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment:**
   ```bash
   cp config/.env.example .env
   # Edit .env with your settings
   ```

3. **Run the Application:**
   ```bash
   # Test script
   python main.py
   
   # Or start API server
   python -m uvicorn api_server:app --reload
   ```

## Development Mode

By default, the application runs in **mock mode** (no BigQuery or external API calls required). This allows you to:

- Test the complete workflow
- Develop and debug nodes
- Verify graph routing logic

## Production Mode

To switch to production mode with real BigQuery:

1. Set `USE_MOCK_INTERNAL=false` in `config/.env`
2. Configure BigQuery credentials in `config/.env`
3. Update SQL queries in `src/tools/sql_queries/metric_queries.py` with your actual table names

## Testing

Run the test suite:

```bash
pytest tests/
```

## Key Components

- **State Management**: `src/state/agent_state.py` - TypedDict for workflow state
- **Tools**: `src/tools/` - Internal SQL and External API tools
- **Nodes**: `src/nodes/` - Workflow processing nodes
- **Graph**: `src/graph/workflow.py` - LangGraph workflow construction
- **API Server**: `api_server.py` - FastAPI REST API wrapper

## Docker Support

This project is fully dockerized for easy deployment:

- **Dockerfile**: Production-ready container with Python 3.10
- **docker-compose.yml**: Orchestrates backend and frontend services
- **PostgreSQL Integration**: Connects to PostgreSQL on host machine via host network mode
- **Health Checks**: Built-in health monitoring for container orchestration

**Configuration:**
- Backend uses `network_mode: host` to access PostgreSQL on `localhost:5432`
- Frontend runs on port 3000 (mapped from container port 80)
- Environment variables are read from `.env` file

## Next Steps

1. Integrate real BigQuery client
2. Add LLM integration for classifier and analyst nodes
3. Implement real external API calls
4. Add more insights (complete 1-18 mapping)
5. Add frontend integration

## License

[Add your license here]

