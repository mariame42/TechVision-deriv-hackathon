"""
Node F: The Analyst (Root Cause Engine)

Generates the JSON narrative using Raw + Derived Data.
Uses LLM to create human-readable insights from the collected data.
"""

import json
from ..state import AgentState


def node_analyst(state: AgentState) -> AgentState:
    """
    Generates the Narrative using Raw + Derived Data.
    
    The LLM sees both fetched_data and derived_data to generate
    a comprehensive business insight.
    
    Args:
        state: The current agent state
        
    Returns:
        Updated state with final_response containing the insight
    """
    print(f"--- ANALYST: Generating Insight for #{state.get('mapped_insight_id')} ---")
    
    # The LLM now sees the Math results too!
    fetched_data = state.get("fetched_data", {})
    derived_data = state.get("derived_data", {})
    data_context = {**fetched_data, **derived_data}
    
    # TODO: Replace with actual LLM call (Gemini/Vertex AI)
    # For now, using simulated response
    # In production, this would use LangChain PromptTemplate + LLM
    
    # SIMULATED LLM RESPONSE
    narrative = _generate_simulated_insight(
        user_query=state.get("user_query", ""),
        insight_id=state.get("mapped_insight_id"),
        insight_name=state.get("insight_name", ""),
        data_context=data_context
    )
    
    return {"final_response": narrative}


def _generate_simulated_insight(
    user_query: str,
    insight_id: int,
    insight_name: str,
    data_context: dict
) -> dict:
    """
    Generate a simulated insight (temporary until LLM is integrated).
    
    Args:
        user_query: The user's original question
        insight_id: The mapped insight ID
        insight_name: The insight name
        data_context: Combined fetched and derived data
        
    Returns:
        Dictionary with headline, analysis, action_item, sentiment
    """
    # Example logic based on data
    revenue = data_context.get("internal_revenue", 0)
    volatility_ratio = data_context.get("volatility_ratio", 0)
    btc_price = data_context.get("external_btc_price", 0)
    
    if volatility_ratio > 1.5:
        headline = "Revenue Stable Relative to Market Volatility"
        analysis = f"While revenue is at ${revenue:,.0f}, the Market/Internal Volatility Ratio is {volatility_ratio} (High). This indicates we are shielding users from broader market chaos."
        sentiment = "positive"
    elif revenue < 1000000:
        headline = "Revenue Dip Driven by External Crypto Correction"
        analysis = f"Internal revenue dropped to ${revenue:,.0f}, closely mirroring market conditions (BTC: ${btc_price:,.0f}). System latency remains stable, ruling out platform infrastructure issues."
        sentiment = "neutral"
    else:
        headline = "Revenue Performance Analysis"
        analysis = f"Revenue stands at ${revenue:,.0f} with market volatility ratio of {volatility_ratio}. System is performing within expected parameters."
        sentiment = "neutral"
    
    return {
        "headline": headline,
        "analysis": analysis,
        "action_item": "Monitor market conditions and continue tracking key metrics.",
        "sentiment": sentiment,
        "data": data_context  # Include raw data for frontend visualization
    }

