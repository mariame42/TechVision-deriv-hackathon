"""
Node D: The Hybrid Data Fetcher

Iterates through required metrics and routes them to the correct tool:
- Metrics starting with "internal_" -> SQL tool
- Metrics starting with "external_" -> API tool
"""

from ..state import AgentState
from ..tools import get_internal_tool, get_external_tool


def node_hybrid_fetcher(state: AgentState) -> AgentState:
    """
    Fetches Raw Data (SQL + API).
    
    Smart routing based on metric prefix:
    - "internal_*" -> InternalMetricTool (SQL/BigQuery)
    - "external_*" -> ExternalMarketTool (APIs)
    
    Args:
        state: The current agent state
        
    Returns:
        Updated state with fetched_data and errors
    """
    print(f"--- FETCHER: Getting {len(state.get('required_metrics', []))} metrics ---")
    
    required_metrics = state.get("required_metrics", [])
    current_data = state.get("fetched_data", {}).copy()
    errors = state.get("errors", []).copy()
    
    internal_tool = get_internal_tool()
    external_tool = get_external_tool()
    
    for metric in required_metrics:
        try:
            val = None
            
            # ROUTING LOGIC: Check prefix to decide tool
            if metric.startswith("internal_"):
                val = internal_tool.fetch_metric(metric)
            elif metric.startswith("external_"):
                val = external_tool.fetch_metric(metric)
            else:
                errors.append(f"Metric '{metric}' has unknown prefix. Must start with 'internal_' or 'external_'")
            
            # DATA MERGING
            if val is not None:
                current_data[metric] = val
            else:
                errors.append(f"Missing data for {metric}")
                
        except Exception as e:
            errors.append(f"Failed to fetch {metric}: {str(e)}")
    
    return {
        "fetched_data": current_data,
        "errors": errors
    }

