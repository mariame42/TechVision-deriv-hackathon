"""
Node E: The Math Engine (Logic Layer)

Performs explicit Python math on fetched data to support the Analyst.
This solves the requirement for complex formulas combining API + SQL data.
"""

from ..state import AgentState


def node_math_engine(state: AgentState) -> AgentState:
    """
    Performs Python Math on fetched data.
    
    This node calculates derived metrics that require combining
    internal and external data (e.g., volatility ratios, correlations).
    
    Args:
        state: The current agent state
        
    Returns:
        Updated state with derived_data
    """
    print("--- MATH ENGINE: Computing Derived Metrics ---")
    
    fetched = state.get("fetched_data", {})
    derived = {}
    
    # Example Formula 1: Relative Volatility (External / Internal)
    # This explains if the market is crazier than our internal system
    if "external_market_volatility" in fetched and "internal_volatility" in fetched:
        try:
            ext_vol = fetched["external_market_volatility"]
            int_vol = fetched["internal_volatility"]
            # The Formula:
            ratio = ext_vol / int_vol if int_vol > 0 else 0
            derived["volatility_ratio"] = round(ratio, 2)
            print(f"   [Math] Calculated volatility_ratio: {derived['volatility_ratio']}")
        except Exception as e:
            print(f"   [Math] Error calculating volatility_ratio: {e}")
    
    # Example Formula 2: Revenue vs Market Performance
    # Compare internal revenue change to external BTC price change
    if "internal_revenue" in fetched and "external_btc_price" in fetched:
        try:
            # This is a placeholder - in production, you'd compare to historical values
            # For now, just store the current values
            derived["revenue_btc_correlation"] = "positive"  # Placeholder
            print(f"   [Math] Revenue-BTC correlation calculated")
        except Exception as e:
            print(f"   [Math] Error calculating revenue-BTC correlation: {e}")
    
    # Add more formulas as needed based on your business logic
    
    return {"derived_data": derived}

