# Project Structure Documentation

## Overview

This document defines the file structure for the Trading Analytics Platform. The architecture is designed to support both mock data (for development) and real BigQuery integration (for production), with clean separation of concerns.

## Directory Structure

```
TechVision-deriv-hackathon/
├── src/                              # Main source code
│   ├── __init__.py
│   │
│   ├── state/                        # State management
│   │   ├── __init__.py
│   │   └── agent_state.py            # AgentState TypedDict definition
│   │
│   ├── tools/                        # Data fetching tools
│   │   ├── __init__.py
│   │   ├── base.py                   # Abstract base classes for tools
│   │   ├── internal_metrics.py       # Internal SQL tool (mock/real switch)
│   │   ├── external_apis.py          # External API tool (mock/real switch)
│   │   └── sql_queries/              # SQL query definitions
│   │       ├── __init__.py
│   │       └── metric_queries.py     # SQL formulas mapped to metric keys
│   │
│   ├── nodes/                        # LangGraph workflow nodes
│   │   ├── __init__.py
│   │   ├── dispatcher.py             # Node A: Entry point router
│   │   ├── batch_loader.py           # Node B: Fast dashboard loader
│   │   ├── classifier.py             # Node C: Intent classifier
│   │   ├── hybrid_fetcher.py         # Node D: Hybrid data fetcher
│   │   ├── math_engine.py            # Node E: Math calculations
│   │   └── analyst.py                # Node F: LLM analysis engine
│   │
│   ├── graph/                        # LangGraph workflow
│   │   ├── __init__.py
│   │   └── workflow.py               # Graph construction and wiring
│   │
│   ├── config/                       # Configuration management
│   │   ├── __init__.py
│   │   ├── settings.py               # App settings and environment vars
│   │   └── insights.py               # Insight ID mappings (1-18)
│   │
│   └── utils/                        # Utility functions
│       ├── __init__.py
│       └── logging.py                # Logging configuration
│
├── tests/                            # Test suite
│   ├── __init__.py
│   ├── test_tools.py                 # Tool tests
│   ├── test_nodes.py                 # Node tests
│   └── test_graph.py                 # Graph integration tests
│
├── config/                           # Configuration files
│   ├── .env.example                  # Example environment variables
│   └── bigquery_config.yaml          # BigQuery project/dataset config
│
├── requirements.txt                  # Python dependencies
├── .gitignore                        # Git ignore rules
├── README.md                         # Project README
├── main.py                           # Application entry point
└── PROJECT_STRUCTURE.md              # This file
```

## Component Descriptions

### `/src/state/`
- **Purpose**: Defines the shared state structure used throughout the LangGraph workflow
- **Key File**: `agent_state.py` - Contains the `AgentState` TypedDict with all fields (request_type, chat_history, fetched_data, derived_data, etc.)

### `/src/tools/`
- **Purpose**: Data fetching layer with abstraction for mock vs. real implementations
- **Key Files**:
  - `base.py`: Abstract base classes (`BaseInternalTool`, `BaseExternalTool`) for easy switching between mock and real
  - `internal_metrics.py`: Internal SQL tool that can use mock data or real BigQuery
  - `external_apis.py`: External API tool for market data (Bloomberg, CoinGecko, etc.)
  - `sql_queries/metric_queries.py`: All SQL query strings mapped to metric keys (ready for BigQuery)

### `/src/nodes/`
- **Purpose**: Individual workflow nodes that process the state
- **Key Files**:
  - `dispatcher.py`: Routes requests (dashboard_load vs chat_query)
  - `batch_loader.py`: Fast path for dashboard overview cards
  - `classifier.py`: Maps user queries to Insight IDs (1-18)
  - `hybrid_fetcher.py`: Routes metrics to appropriate tools (SQL or API)
  - `math_engine.py`: Performs Python calculations on combined data
  - `analyst.py`: Generates LLM-powered insights

### `/src/graph/`
- **Purpose**: LangGraph workflow construction and wiring
- **Key File**: `workflow.py` - Builds the StateGraph, adds nodes, defines edges, and compiles the app

### `/src/config/`
- **Purpose**: Configuration and constants
- **Key Files**:
  - `settings.py`: Environment variables, feature flags, BigQuery credentials
  - `insights.py`: Mapping of Insight IDs (1-18) to names and required metrics

### `/src/utils/`
- **Purpose**: Shared utility functions
- **Key File**: `logging.py` - Centralized logging configuration

### `/tests/`
- **Purpose**: Unit and integration tests
- **Structure**: Mirrors `/src/` structure for easy test organization

### `/config/`
- **Purpose**: Configuration files (not Python code)
- **Key Files**:
  - `.env.example`: Template for environment variables
  - `bigquery_config.yaml`: BigQuery project, dataset, and table configurations

## Design Principles

1. **Separation of Concerns**: Each component has a single, well-defined responsibility
2. **Mock/Real Abstraction**: Tools use base classes to easily switch between mock and production implementations
3. **BigQuery Ready**: SQL queries are separated and ready for direct BigQuery integration
4. **Testability**: Clear structure makes it easy to write and maintain tests
5. **Scalability**: Modular design allows easy addition of new metrics, insights, or nodes

## Integration Points

### BigQuery Integration
- **Mock Mode**: `tools/internal_metrics.py` uses in-memory dictionaries
- **Real Mode**: Same file switches to `google-cloud-bigquery` client using queries from `sql_queries/metric_queries.py`
- **Switch**: Controlled via environment variable in `config/settings.py`

### External APIs
- **Mock Mode**: `tools/external_apis.py` uses mock responses
- **Real Mode**: Makes actual HTTP requests to Bloomberg, CoinGecko, etc.
- **Switch**: Controlled via environment variable in `config/settings.py`

## Next Steps

1. Create all directory structure
2. Implement base classes and abstractions
3. Build mock implementations first
4. Add BigQuery integration layer
5. Wire up the complete graph
6. Add tests
