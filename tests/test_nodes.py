"""
Tests for workflow nodes.
"""

import pytest
from src.state import AgentState
from src.nodes import (
    node_dispatcher,
    node_batch_loader,
    node_classifier,
    node_hybrid_fetcher,
    node_math_engine,
)


def test_node_dispatcher():
    """Test dispatcher node."""
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
    result = node_dispatcher(state)
    assert "errors" in result
    assert "fetched_data" in result


def test_node_batch_loader():
    """Test batch loader node."""
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
    result = node_batch_loader(state)
    assert "fetched_data" in result
    assert "final_response" in result

