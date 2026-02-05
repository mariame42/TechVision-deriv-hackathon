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
- **Data Source**: BigQuery (Mocked for development) & External Market APIs

## Project Structure

See [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md) for detailed documentation.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy the example environment file and configure it:

```bash
cp config/.env.example config/.env
# Edit config/.env with your settings
```

### 3. Run the Application

```bash
python main.py
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

## Next Steps

1. Integrate real BigQuery client
2. Add LLM integration for classifier and analyst nodes
3. Implement real external API calls
4. Add more insights (complete 1-18 mapping)
5. Add frontend integration

## License

[Add your license here]

