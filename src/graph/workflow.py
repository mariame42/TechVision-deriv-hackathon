"""
LangGraph workflow construction and wiring.

This module builds the StateGraph, adds all nodes, defines edges,
and compiles the final application.
"""

from langgraph.graph import StateGraph, END
from ..state import AgentState
from ..nodes import (
    node_dispatcher,
    node_batch_loader,
    node_classifier,
    node_hybrid_fetcher,
    node_math_engine,
    node_analyst,
)

# Global app instance
_app = None


def create_app() -> StateGraph:
    """
    Create and configure the LangGraph workflow.
    
    Returns:
        Compiled StateGraph application
    """
    # --- Graph Construction ---
    workflow = StateGraph(AgentState)
    
    # Add Nodes
    workflow.add_node("dispatcher", node_dispatcher)
    workflow.add_node("batch_loader", node_batch_loader)
    workflow.add_node("classifier", node_classifier)
    workflow.add_node("fetcher", node_hybrid_fetcher)
    workflow.add_node("math_engine", node_math_engine)
    workflow.add_node("analyst", node_analyst)
    
    # Set Entry Point
    workflow.set_entry_point("dispatcher")
    
    # Routing Logic
    def route_request(state: AgentState) -> str:
        """Route based on request_type."""
        return "batch_loader" if state["request_type"] == "dashboard_load" else "classifier"
    
    workflow.add_conditional_edges(
        "dispatcher",
        route_request,
        {
            "batch_loader": "batch_loader",
            "classifier": "classifier"
        }
    )
    
    # Chat Flow: classifier -> fetcher -> math_engine -> analyst -> END
    workflow.add_edge("classifier", "fetcher")
    workflow.add_edge("fetcher", "math_engine")
    workflow.add_edge("math_engine", "analyst")
    workflow.add_edge("analyst", END)
    
    # Dashboard Flow: batch_loader -> END
    workflow.add_edge("batch_loader", END)
    
    # Compile
    app = workflow.compile()
    return app


def get_app() -> StateGraph:
    """
    Get the global app instance (singleton pattern).
    
    Returns:
        Compiled StateGraph application
    """
    global _app
    if _app is None:
        _app = create_app()
    return _app

