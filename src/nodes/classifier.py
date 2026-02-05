"""
Node C: Intent Classifier (Chat Path)

Maps user questions to Insight IDs (1-18) and determines required metrics.
Uses LLM to understand user intent and route to appropriate analysis.
"""

from ..state import AgentState
from ..config.insights import INSIGHT_MAP


def node_classifier(state: AgentState) -> AgentState:
    """
    Identifies the Insight ID and the metrics needed.
    
    Includes context from chat_history if needed.
    Uses LLM to map natural language to one of the 18 Insights.
    
    Args:
        state: The current agent state
        
    Returns:
        Updated state with mapped_insight_id, insight_name, and required_metrics
    """
    query = state.get("user_query", "")
    print(f"--- CLASSIFIER: Processing '{query}' ---")
    
    # TODO: Replace with actual LLM classification
    # For now, using simple keyword matching as simulation
    # In production, this would use LangChain + LLM to classify intent
    
    # SIMULATED LLM DECISION
    # Example: "Why did we lose money?" -> Insight 17
    insight_id = _classify_intent_simple(query)
    insight_info = INSIGHT_MAP.get(insight_id, {})
    
    return {
        "mapped_insight_id": insight_id,
        "insight_name": insight_info.get("name", "General Analysis"),
        "required_metrics": insight_info.get("required_metrics", []),
    }


def _classify_intent_simple(query: str) -> int:
    """
    Simple keyword-based classification (temporary until LLM is integrated).
    
    Args:
        query: User's question
        
    Returns:
        Insight ID (1-18)
    """
    query_lower = query.lower()
    
    # Simple keyword matching (replace with LLM in production)
    if any(word in query_lower for word in ["lose", "lost", "money", "revenue", "drop", "down"]):
        return 17  # Revenue Drop Root Cause
    elif any(word in query_lower for word in ["volatility", "volatile", "vol"]):
        return 1  # Volatility Analysis (example)
    else:
        return 1  # Default to general analysis
