"""
Node F: The Analyst (Root Cause Engine)

Generates the JSON narrative using Raw + Derived Data.
Uses LLM to create human-readable insights from the collected data.
"""

import json
from ..state import AgentState


def node_analyst(state: AgentState) -> AgentState:
    """
    Extracts the calculated number from derived_data and returns it.
    
    For now, returns only the numeric result from the insights pipeline.
    
    Args:
        state: The current agent state
        
    Returns:
        Updated state with final_response containing just the number
    """
    print(f"--- ANALYST: Extracting result for Insight #{state.get('mapped_insight_id')} ---")
    
    derived_data = state.get("derived_data", {})
    
    # Extract the first numeric value from derived_data
    result_value = None
    
    if derived_data:
        print(f"   [Analyst] derived_data keys: {list(derived_data.keys())}")
        print(f"   [Analyst] derived_data values: {list(derived_data.values())}")
        
        # Get the first value from derived_data
        first_key = list(derived_data.keys())[0] if derived_data else None
        if first_key:
            result_value = derived_data[first_key]
            print(f"   [Analyst] First key: {first_key}, value: {result_value}, type: {type(result_value).__name__}")
            
            # If it's a dict (like revenue_drop_root_cause), get the first numeric value
            if isinstance(result_value, dict):
                for key, value in result_value.items():
                    if isinstance(value, (int, float)) and not (isinstance(value, float) and (value != value or value == float('inf'))):  # Check for NaN/inf
                        result_value = float(value)  # Convert numpy types to Python float
                        print(f"   [Analyst] Extracted from dict: {key} = {result_value}")
                        break
            # If it's already a number, use it directly
            elif isinstance(result_value, (int, float)):
                # Handle numpy types
                if hasattr(result_value, 'item'):
                    result_value = result_value.item()  # Convert numpy scalar to Python type
                result_value = float(result_value)  # Ensure it's a Python float
                print(f"   [Analyst] Using numeric value: {result_value}")
            else:
                result_value = None
                print(f"   [Analyst] Value is not numeric: {type(result_value)}")
    else:
        print(f"   [Analyst] WARNING: derived_data is empty!")
    
    print(f"   [Analyst] Extracted result value: {result_value}")
    
    # Return simple response with just the number
    return {
        "final_response": {
            "value": result_value if result_value is not None else 0,
            "headline": "",
            "analysis": "",
            "action_item": "",
            "sentiment": "neutral",
            "data": derived_data  # Keep data for debugging
        }
    }



