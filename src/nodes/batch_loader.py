"""
Node B: Batch Loader (Fast Path)

This node populates the 6 Domain Health Cards for dashboard overview.
Pure data fetching, no LLM reasoning for speed.
"""

from ..state import AgentState
from ..tools import get_internal_tool


def node_batch_loader(state: AgentState) -> AgentState:
    """
    Fast Dashboard Loader.
    
    Fetches the 6 key metrics for the Domain Health Overview cards.
    These are hardcoded because they ALWAYS load on the dashboard.
    
    Args:
        state: The current agent state
        
    Returns:
        Updated state with fetched_data and final_response
    """
    print("--- 2A. BATCH LOADER: Fetching Overview Cards ---")
    
    # These are the 6 headline metrics for the dashboard
    overview_metrics = [
        "internal_arpu",
        "internal_vip_retention",
        "internal_revenue",
        "internal_latency",
        "internal_volatility",
        "internal_churn",
    ]
    
    internal_tool = get_internal_tool()
    data = {}
    
    for metric in overview_metrics:
        value = internal_tool.fetch_metric(metric)
        if value is not None:
            data[metric] = value
    
    return {
        "fetched_data": data,
        "final_response": {
            "type": "dashboard_view",
            "cards": data
        }
    }
