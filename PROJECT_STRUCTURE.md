# Project Structure Documentation

## Overview

This document defines the file structure for the Trading Analytics Platform. The architecture is designed to support PostgreSQL as the primary data source, with a unified Python pipeline for data processing and insights computation.

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
│   ├── db/                           # Database layer
│   │   ├── __init__.py
│   │   └── postgres_connector.py      # PostgreSQL connection handler
│   │
│   ├── preprocessing/                # Data preprocessing
│   │   ├── __init__.py
│   │   └── data_preprocessor.py      # Data fetching and cleaning with Pandas
│   │
│   ├── insights/                     # Insights computation
│   │   ├── __init__.py
│   │   └── insights_engine.py        # All insight calculation logic
│   │
│   ├── nodes/                        # LangGraph workflow nodes
│   │   ├── __init__.py
│   │   ├── dispatcher.py             # Node A: Entry point router
│   │   ├── batch_loader.py           # Node B: Fast dashboard loader
│   │   ├── classifier.py             # Node C: Intent classifier (LLM/keyword)
│   │   ├── insights_pipeline.py      # Node D: Unified data pipeline
│   │   └── analyst.py                # Node F: LLM analysis engine
│   │
│   ├── graph/                        # LangGraph workflow
│   │   ├── __init__.py
│   │   └── workflow.py               # Graph construction and wiring
│   │
│   ├── config/                       # Configuration management
│   │   ├── __init__.py
│   │   ├── settings.py               # App settings and environment vars
│   │   └── insights.py               # Insight ID mappings (1-18) with reasoning data
│   │
│   ├── tools/                        # Legacy tools (deprecated)
│   │   ├── __init__.py
│   │   ├── base.py                   # Abstract base classes for tools
│   │   ├── internal_metrics.py       # Internal SQL tool (legacy)
│   │   ├── external_apis.py          # External API tool (legacy)
│   │   └── sql_queries/               # SQL query definitions (legacy)
│   │       ├── __init__.py
│   │       └── metric_queries.py     # SQL formulas mapped to metric keys
│   │
│   └── utils/                        # Utility functions
│       ├── __init__.py
│       └── logging.py                # Logging configuration
│
├── frontend/                         # React frontend application
│   ├── src/
│   │   ├── components/
│   │   │   ├── layout/               # MainLayout, Sidebar, Topbar
│   │   │   ├── dashboard/            # MetricCard, InsightBanner
│   │   │   └── chat/                 # ChatInterface, MessageList, InputBox
│   │   ├── pages/                    # DashboardPage, etc.
│   │   ├── services/                 # api.ts - Backend API integration
│   │   └── App.tsx                   # Main app with routing
│   ├── Dockerfile                    # Multi-stage build with Nginx
│   ├── nginx.conf                    # Nginx configuration
│   ├── package.json                  # Dependencies
│   └── README.md                     # Frontend documentation
│
├── tests/                            # Test suite
│   ├── __init__.py
│   ├── test_tools.py                 # Tool tests
│   ├── test_nodes.py                 # Node tests
│   └── test_graph.py                 # Graph integration tests
│
├── requirements.txt                  # Python dependencies
├── .env.example                      # Example environment variables
├── .gitignore                        # Git ignore rules
├── README.md                         # Project README
├── main.py                           # Application entry point
├── api_server.py                     # FastAPI REST API server
├── debug_pipeline.py                 # Diagnostic script for pipeline
├── Dockerfile                        # Backend Dockerfile
├── docker-compose.yml                # Docker Compose configuration
└── PROJECT_STRUCTURE.md              # This file
```

## Component Descriptions

### `/src/state/`
- **Purpose**: Defines the shared state structure used throughout the LangGraph workflow
- **Key File**: `agent_state.py` - Contains the `AgentState` TypedDict with all fields (request_type, chat_history, mapped_insight_id, insight_name, fetched_data, derived_data, final_response, etc.)

### `/src/db/`
- **Purpose**: Database connection and management
- **Key File**: `postgres_connector.py` - Handles PostgreSQL connections using psycopg2, reads credentials from environment variables

### `/src/preprocessing/`
- **Purpose**: Data fetching and cleaning
- **Key File**: `data_preprocessor.py` - Uses Pandas to fetch data from PostgreSQL tables, handles missing values, and provides data cleaning utilities

### `/src/insights/`
- **Purpose**: Core business logic for computing insights
- **Key File**: `insights_engine.py` - Implements all 7 active insights as Python methods:
  - `trading_revenue_change()` - Day-over-day revenue percentage
  - `revenue_sensitivity_to_volatility()` - Correlation analysis
  - `active_trader_change()` - Trader count changes
  - `volatility_regime_shift()` - Volatility regime detection
  - `volume_contraction()` - Volume decline detection
  - `asset_rotation_detection()` - Asset flow analysis
  - `revenue_drop_root_cause()` - Multi-factor root cause analysis

### `/src/nodes/`
- **Purpose**: Individual workflow nodes that process the state
- **Key Files**:
  - `dispatcher.py`: Routes requests (dashboard_load vs chat_query)
  - `batch_loader.py`: Fast path for dashboard overview cards (SQL queries)
  - `classifier.py`: Maps user queries to Insight IDs (1-18) using OpenRouter LLM or keyword matching
  - `insights_pipeline.py`: Unified pipeline that:
    - Connects to PostgreSQL
    - Fetches and preprocesses data
    - Computes insights using InsightsEngine
    - Returns derived_data to state
  - `analyst.py`: Generates final response with:
    - Headline (includes insight ID and name)
    - Analysis (based on "Goes Up When", "Goes Down When", or "zero because" from insights config)
    - Action items
    - Sentiment

### `/src/graph/`
- **Purpose**: LangGraph workflow construction and wiring
- **Key File**: `workflow.py` - Builds the StateGraph, adds nodes, defines edges:
  - Dashboard path: `dispatcher → batch_loader → END`
  - Chat path: `dispatcher → classifier → insights_pipeline → analyst → END`

### `/src/config/`
- **Purpose**: Configuration and constants
- **Key Files**:
  - `settings.py`: Environment variables, PostgreSQL credentials, LLM configuration (OpenRouter)
  - `insights.py`: Mapping of Insight IDs (1-18) to names and reasoning data:
    - "Goes Up When" - Array of reasons for positive values
    - "Goes Down When" - Array of reasons for negative values
    - "zero because" - Explanation for zero values

### `/src/tools/` (Legacy)
- **Purpose**: Legacy tools for BigQuery and external APIs (deprecated)
- **Status**: These tools are no longer used in the main workflow but kept for reference
- **Note**: The new pipeline uses PostgreSQL directly via `db/postgres_connector.py`

### `/src/utils/`
- **Purpose**: Shared utility functions
- **Key File**: `logging.py` - Centralized logging configuration

### `/frontend/`
- **Purpose**: React frontend application
- **Structure**:
  - `src/components/` - Reusable UI components
  - `src/pages/` - Page components (Dashboard, Chat)
  - `src/services/` - API integration layer
  - `Dockerfile` - Multi-stage build (build + nginx serve)
  - `nginx.conf` - Nginx configuration for SPA

### `/tests/`
- **Purpose**: Unit and integration tests
- **Structure**: Mirrors `/src/` structure for easy test organization

## Data Flow

### Dashboard Load Flow
```
User Request → Dispatcher → Batch Loader → PostgreSQL → Return 6 Metrics
```

### Chat Query Flow
```
User Query → Dispatcher → Classifier (LLM/Keyword) → Insights Pipeline → Analyst → Response
                                                          ↓
                                              PostgreSQL → Preprocessing → Insights Engine
```

## Design Principles

1. **Separation of Concerns**: Each component has a single, well-defined responsibility
2. **PostgreSQL First**: All data comes from PostgreSQL, no external API dependencies
3. **Python-Based Calculations**: All insights computed in Python, no external formulas
4. **Unified Pipeline**: Single `insights_pipeline` node replaces separate fetcher and math engine
5. **LLM Integration**: OpenRouter API for classification and future analysis generation
6. **Testability**: Clear structure makes it easy to write and maintain tests
7. **Scalability**: Modular design allows easy addition of new insights or nodes

## Integration Points

### PostgreSQL Integration
- **Connection**: `src/db/postgres_connector.py` handles all database connections
- **Data Fetching**: `src/preprocessing/data_preprocessor.py` uses Pandas to query tables
- **Tables Used**: `daily_revenue`, `client_activity`, `market_prices`
- **Configuration**: Database credentials via environment variables in `.env`

### LLM Integration
- **Provider**: OpenRouter API
- **Usage**: 
  - Classification in `classifier.py` (optional, falls back to keywords)
  - Future: Analysis generation in `analyst.py` (via `prosses_reasoning_data_and_llm`)
- **Configuration**: API key and model via environment variables

### Frontend Integration
- **API Endpoints**: 
  - `POST /api/dashboard/load` - Dashboard metrics
  - `POST /api/chat/query` - Chat queries
- **Response Format**: JSON with `value`, `headline`, `analysis`, `action_item`, `sentiment`

## Next Steps

1. Complete LLM integration for `prosses_reasoning_data_and_llm` function
2. Implement remaining insights (8-18)
3. Add more sophisticated analysis generation
4. Enhance frontend with visualization components
5. Add real-time data streaming capabilities
