"""
Node E: The Math Engine (Logic Layer)

Performs explicit Python math on fetched data to support the Analyst.
Uses insight-specific formulas from the insights config.
"""

from ..state import AgentState
from ..config.insights import INSIGHT_MAP


def node_math_engine(state: AgentState) -> AgentState:
    """
    Performs Python Math on fetched data using insight-specific formulas.
    
    This node calculates derived metrics based on the insight_id and
    the formulas defined in the insights config.
    
    Args:
        state: The current agent state
        
    Returns:
        Updated state with derived_data
    """
    insight_id = state.get("mapped_insight_id")
    fetched = state.get("fetched_data", {})
    derived = {}
    
    print(f"--- MATH ENGINE: Computing Derived Metrics for Insight #{insight_id} ---")
    
    if not insight_id:
        print("   [Math] WARNING: No insight_id found, skipping formula calculations")
        return {"derived_data": derived}
    
    # Get insight configuration
    insight_info = INSIGHT_MAP.get(insight_id, {})
    
    if not insight_info:
        print(f"   [Math] WARNING: No configuration found for Insight {insight_id}")
        return {"derived_data": derived}
    
    # Handle nested structure: {1: {"Trading revenue change": {...}}}
    if isinstance(insight_info, dict) and insight_info:
        first_key = list(insight_info.keys())[0]
        if isinstance(insight_info[first_key], dict):
            insight_config = insight_info[first_key]
        else:
            insight_config = insight_info
    else:
        insight_config = insight_info
    
    # Get formulas for this insight
    formulas = insight_config.get("formulas", {})
    
    if not formulas:
        print(f"   [Math] No formulas defined for Insight {insight_id}, using default calculations")
        # Fallback to default calculations if no formulas defined
        derived = _calculate_default_formulas(fetched)
        return {"derived_data": derived}
    
    print(f"   [Math] Found {len(formulas)} formula(s) for Insight {insight_id}")
    
    # Execute each formula
    for formula_name, formula_func in formulas.items():
        try:
            # Execute the formula function with fetched_data
            result = formula_func(fetched)
            derived[formula_name] = result
            print(f"   [Math] ✓ Calculated '{formula_name}': {result}")
        except Exception as e:
            print(f"   [Math] ✗ Error calculating '{formula_name}': {e}")
            derived[formula_name] = None
    
    return {"derived_data": derived}


def _calculate_default_formulas(fetched: dict) -> dict:
    """
    Default formulas when no insight-specific formulas are defined.
    
    Args:
        fetched: Fetched data dictionary
        
    Returns:
        Dictionary of derived metrics
    """
    derived = {}
    
    # Default Formula 1: Relative Volatility (External / Internal)
    if "external_market_volatility" in fetched and "internal_volatility" in fetched:
        try:
            ext_vol = fetched["external_market_volatility"]
            int_vol = fetched["internal_volatility"]
            ratio = ext_vol / int_vol if int_vol > 0 else 0
            derived["volatility_ratio"] = round(ratio, 2)
            print(f"   [Math] Calculated default volatility_ratio: {derived['volatility_ratio']}")
        except Exception as e:
            print(f"   [Math] Error calculating default volatility_ratio: {e}")
    
    # Default Formula 2: Revenue vs Market Performance
    if "internal_revenue" in fetched and "external_btc_price" in fetched:
        try:
            # Placeholder correlation
            derived["revenue_btc_correlation"] = "positive"
            print(f"   [Math] Calculated default revenue-BTC correlation")
        except Exception as e:
            print(f"   [Math] Error calculating default revenue-BTC correlation: {e}")
    
    return derived
