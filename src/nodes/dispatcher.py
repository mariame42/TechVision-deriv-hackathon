"""
Node A: The Dispatcher (Entry Point)

This node routes requests based on request_type:
- "dashboard_load" -> routes to batch_loader (fast path)
- "chat_query" -> routes to classifier (smart path)
"""

from ..state import AgentState


def node_dispatcher(state: AgentState) -> AgentState:
    """
    Entry point: Routes based on request type.
    
    This node initializes default values and passes through to
    conditional routing logic in the graph.
    
    Args:
        state: The current agent state
        
    Returns:
        Updated state with initialized fields
    """
    print(f"--- 1. DISPATCHER: Received {state['request_type']} ---")
    
    # Initialize default values if not present
    return {
        "errors": state.get("errors", []),
        "fetched_data": state.get("fetched_data", {}),
        "derived_data": state.get("derived_data", {}),
    }
