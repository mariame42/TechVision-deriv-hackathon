# Trading Analytics Platform

A sophisticated AI-driven analytics platform for trading companies, built with LangGraph, React, and PostgreSQL.

## Architecture

This platform differentiates between two primary workflows:

1. **Dashboard Load (Fast Path)**: High-speed SQL-only path to load static overview cards
2. **Chat Query (Smart Path)**: Deep-reasoning path involving PostgreSQL queries, insights computation, and LLM analysis

## Tech Stack

### Backend
- **Orchestration**: LangGraph
- **Tools**: LangChain
- **Language**: Python 3.10+
- **Data Source**: PostgreSQL (primary)
- **LLM**: OpenRouter API (configurable)
- **API Framework**: FastAPI + Uvicorn

### Frontend
- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS (dark mode)
- **Routing**: React Router

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **Database**: PostgreSQL
- **Web Server**: Nginx (frontend)

## Project Structure

See [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md) for detailed documentation.

## Quick Start

### Option A: Docker (Recommended)

**Fastest way to get started with a production-like setup:**

1. **Configure Environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your PostgreSQL credentials and OpenRouter API key
   ```

2. **Ensure PostgreSQL is Running:**
   - PostgreSQL should be accessible on `localhost:5432`
   - Database should be created and populated with trading data

3. **Run with Docker:**
   ```bash
   docker-compose up --build
   ```

4. **Access the Application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Health check: http://localhost:8000/health

**Note:** Docker backend uses host network mode to connect to PostgreSQL on the host machine.

### Option B: Local Development

#### Backend Setup

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your settings (PostgreSQL, OpenRouter API key)
   ```

3. **Run the Application:**
   ```bash
   # Test script
   python main.py
   
   # Or start API server
   python -m uvicorn api_server:app --reload
   ```

#### Frontend Setup

1. **Install Dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Configure Environment:**
   ```bash
   # Create .env file in frontend/
   echo "VITE_BACKEND_URL=http://localhost:8000" > .env
   ```

3. **Start Development Server:**
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:3000`

## Workflow Overview

### Dashboard Load Path
```
User Request → Dispatcher → Batch Loader → Return 6 Metric Cards
```

### Chat Query Path
```
User Query → Dispatcher → Classifier → Insights Pipeline → Analyst → Response
```

**Node Details:**
- **Dispatcher**: Routes requests (dashboard_load vs chat_query)
- **Batch Loader**: Fast SQL queries for dashboard metrics
- **Classifier**: Maps user queries to Insight IDs (1-18) using LLM or keyword matching
- **Insights Pipeline**: 
  - Connects to PostgreSQL
  - Preprocesses and cleans data
  - Computes insights using Python-based calculations
  - Returns derived data
- **Analyst**: Generates human-readable analysis with headlines, analysis text, and action items

## Key Components

### Backend Modules

- **State Management**: `src/state/agent_state.py` - TypedDict for workflow state
- **Database**: `src/db/postgres_connector.py` - PostgreSQL connection handler
- **Preprocessing**: `src/preprocessing/data_preprocessor.py` - Data fetching and cleaning
- **Insights Engine**: `src/insights/insights_engine.py` - All insight calculations
- **Nodes**: `src/nodes/` - Workflow processing nodes
  - `dispatcher.py` - Request routing
  - `batch_loader.py` - Dashboard metrics
  - `classifier.py` - Intent classification
  - `insights_pipeline.py` - Unified data pipeline
  - `analyst.py` - Response generation
- **Graph**: `src/graph/workflow.py` - LangGraph workflow construction
- **Config**: `src/config/` - Settings and insight mappings
- **API Server**: `api_server.py` - FastAPI REST API wrapper

### Frontend Components

- **Pages**: Dashboard, Chat interface
- **Components**: Metric cards, insight banners, chat interface
- **Services**: API integration layer
- **Layout**: Sidebar, topbar, main layout

## Insights

The platform supports 18 different insights, with 7 currently implemented:

1. **Trading revenue change** - Day-over-day revenue percentage change
2. **Revenue sensitivity to volatility** - Correlation between revenue and market volatility
3. **Active trader change** - Change in number of active traders
4. **Volatility regime shift** - Detection of volatility regime changes
5. **Volume contraction** - Trading volume decline detection
6. **Asset rotation detection** - Capital flow between asset classes
7. **Revenue drop root cause chain** - Multi-factor analysis of revenue decline

Each insight is computed using Python-based calculations on PostgreSQL data, with LLM-powered analysis for generating human-readable explanations.

## Environment Variables

### Backend (.env)
- `POSTGRES_HOST` - PostgreSQL host (default: localhost)
- `POSTGRES_DATABASE` - Database name
- `POSTGRES_USER` - Database user
- `POSTGRES_PASSWORD` - Database password
- `POSTGRES_PORT` - Database port (default: 5432)
- `OPENROUTER_API_KEY` - OpenRouter API key for LLM
- `LLM_MODEL` - LLM model ID (default: openai/gpt-3.5-turbo)
- `LLM_PROVIDER` - LLM provider (default: openrouter)

### Frontend (.env)
- `VITE_BACKEND_URL` - Backend API URL (default: http://localhost:8000)

## Docker Support

This project is fully dockerized for easy deployment:

- **Backend Dockerfile**: Production-ready container with Python 3.10
- **Frontend Dockerfile**: Multi-stage build with Nginx
- **docker-compose.yml**: Orchestrates backend and frontend services
- **PostgreSQL Integration**: Connects to PostgreSQL on host machine via host network mode
- **Health Checks**: Built-in health monitoring for container orchestration

**Configuration:**
- Backend uses `network_mode: host` to access PostgreSQL on `localhost:5432`
- Frontend runs on port 3000 (mapped from container port 80)
- Environment variables are read from `.env` file

## Development

### Testing

Run the test suite:
```bash
pytest tests/
```

### Debugging

Use `debug_pipeline.py` to diagnose database connectivity and insight calculations:
```bash
python debug_pipeline.py
```

## Next Steps

1. Implement remaining insights (8-18)
2. Complete LLM integration for `prosses_reasoning_data_and_llm` function
3. Add more sophisticated analysis in analyst node
4. Enhance frontend with more visualization components
5. Add real-time data streaming capabilities

## License

[Add your license here]
