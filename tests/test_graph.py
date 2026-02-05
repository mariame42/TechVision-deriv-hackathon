"""
Integration tests for the complete graph workflow.
"""

import pytest
from src.graph import get_app
from src.state import AgentState


def test_dashboard_load_flow():
    """Test the complete dashboard load flow."""
    app = get_app()
    
    inputs: AgentState = {
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
    
    result = app.invoke(inputs)
    assert "final_response" in result
    assert result["final_response"].get("type") == "dashboard_view"


def test_chat_query_flow():
    """Test the complete chat query flow."""
    app = get_app()
    
    inputs: AgentState = {
        "request_type": "chat_query",
        "chat_history": [],
        "user_query": "Why did we lose money?",
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
    
    result = app.invoke(inputs)
    assert "final_response" in result
    assert "headline" in result["final_response"]

