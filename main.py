"""
Trading Analytics Platform - Main Entry Point

This is the application entry point for running the LangGraph workflow.
"""

import json
from src.graph import get_app
from src.state import AgentState
from src.utils.logging import setup_logging


def main():
    """Main entry point for the application."""
    # Setup logging
    setup_logging(level="INFO")
    
    # Get the compiled app
    app = get_app()
    
    # Example 1: Dashboard Load (Fast Path)
    print("\n" + "="*60)
    print(">>> SCENARIO 1: Dashboard Load (Fast Path)")
    print("="*60)
    
    dashboard_input: AgentState = {
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
    
    dashboard_result = app.invoke(dashboard_input)
    print("\n>>> DASHBOARD OUTPUT <<<")
    print(json.dumps(dashboard_result["final_response"], indent=2))
    
    # Example 2: Chat Query (Smart Path)
    print("\n" + "="*60)
    print(">>> SCENARIO 2: Chat Query (Smart Path)")
    print("="*60)
    
    chat_input: AgentState = {
        "request_type": "chat_query",
        "chat_history": [],
        "user_query": "Why did we lose money today?",
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
    
    chat_result = app.invoke(chat_input)
    print("\n>>> CHAT OUTPUT <<<")
    print(json.dumps(chat_result["final_response"], indent=2))
    
    # Example 3: Volatility Comparison Query
    print("\n" + "="*60)
    print(">>> SCENARIO 3: Volatility Comparison Query")
    print("="*60)
    
    volatility_input: AgentState = {
        "request_type": "chat_query",
        "chat_history": [],
        "user_query": "How is our volatility compared to the market?",
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
    
    volatility_result = app.invoke(volatility_input)
    print("\n>>> VOLATILITY ANALYSIS OUTPUT <<<")
    print(json.dumps(volatility_result["final_response"], indent=2))


if __name__ == "__main__":
    main()

