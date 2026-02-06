"""
Trading Analytics Platform - FastAPI Server

This is the production API server that wraps the LangGraph workflow.
It provides REST endpoints for dashboard loading and chat queries.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import json
import logging

from src.graph import get_app
from src.state import AgentState
from src.utils.logging import setup_logging

# Setup logging
setup_logging(level="INFO")
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Trading Analytics Platform API",
    description="AI-driven analytics platform for trading companies",
    version="0.1.0"
)

# CORS middleware (allow frontend to call this API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the LangGraph app
langgraph_app = get_app()


# Request/Response Models
class DashboardLoadRequest(BaseModel):
    """Request model for dashboard load."""
    pass


class ChatQueryRequest(BaseModel):
    """Request model for chat query."""
    user_query: str = Field(..., description="User's question")
    chat_history: Optional[List[Dict[str, Any]]] = Field(
        default=[], 
        description="Previous conversation history"
    )


class AnalyticsResponse(BaseModel):
    """Response model for analytics queries."""
    success: bool
    data: Dict[str, Any]
    errors: List[str] = []


# API Endpoints
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Trading Analytics Platform API",
        "version": "0.1.0",
        "endpoints": {
            "health": "/health",
            "dashboard": "/api/dashboard/load",
            "chat": "/api/chat/query"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for Docker."""
    return {
        "status": "healthy",
        "service": "trading-analytics-backend"
    }


@app.post("/api/dashboard/load", response_model=AnalyticsResponse)
async def dashboard_load(request: DashboardLoadRequest):
    """
    Fast path: Load dashboard overview cards.
    
    This endpoint fetches the 6 key metrics for the dashboard
    without any LLM processing for maximum speed.
    """
    try:
        logger.info("Dashboard load request received")
        
        # Prepare state for dashboard load
        state: AgentState = {
            "request_type": "dashboard_load",
            "chat_history": [],
            "user_query": None,
            "target_domain": None,
            "mapped_insight_id": None,
            "insight_name": None,
            "required_metrics": [],
            "fetched_data": {},
            "derived_data": {},
            "root_cause_analysis": None,
            "final_response": {},
            "errors": [],
        }
        
        # Invoke the LangGraph workflow
        result = langgraph_app.invoke(state)
        
        return AnalyticsResponse(
            success=True,
            data=result.get("final_response", {}),
            errors=result.get("errors", [])
        )
        
    except Exception as e:
        logger.error(f"Error in dashboard load: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/chat/query", response_model=AnalyticsResponse)
async def chat_query(request: ChatQueryRequest):
    """
    Smart path: Process chat query with full LLM analysis.
    
    This endpoint processes user questions through the complete
    pipeline: classification -> data fetching -> math -> analysis.
    """
    try:
        logger.info(f"Chat query received: {request.user_query}")
        
        # Convert chat_history to BaseMessage format if needed
        # For now, keeping it simple - you can enhance this later
        chat_history = []
        
        # Prepare state for chat query
        state: AgentState = {
            "request_type": "chat_query",
            "chat_history": chat_history,
            "user_query": request.user_query,
            "target_domain": None,
            "mapped_insight_id": None,
            "insight_name": None,
            "required_metrics": [],
            "fetched_data": {},
            "derived_data": {},
            "root_cause_analysis": None,
            "final_response": {},
            "errors": [],
        }
        
        # Invoke the LangGraph workflow
        result = langgraph_app.invoke(state)
        
        return AnalyticsResponse(
            success=True,
            data=result.get("final_response", {}),
            errors=result.get("errors", [])
        )
        
    except Exception as e:
        logger.error(f"Error in chat query: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

