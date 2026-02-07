"""
Node F: The Analyst (Root Cause Engine)

Generates the JSON narrative using Raw + Derived Data.
Uses LLM to create human-readable insights from the collected data.
"""

import json
from ..state import AgentState
from ..config.insights import INSIGHT_MAP

def genarate_with_LLM(array_of_data: list) -> str:
    """
    Genarate with LLM
    """
    return "Genarate with LLM"

def check_data(array_of_data: list) -> str:
    """
    Check data
    """
    

    return "Check data"


def prosses_reasoning_data_and_llm(array_of_data: list) -> str:
    """
    Prosses reasoning data and LLM
    """
    remaining_data_array = check_data(array_of_data)
    if remaining_data_array:
        return genarate_with_LLM(remaining_data_array)
    else:
        return "the resone is not found in the data base"
    return "Prosses reasoning data and LLM"


def _analyst_analysis(insight_id: int, insight_name: str, derived_data: dict) -> str:
    """
    Generate analysis text based on insight ID and name.
    
    Args:
        insight_id: The insight ID
        insight_name: The insight name
        derived_data: The derived data dict
    """
    Avalable_Insights = {1, 3, 4, 8, 9}
    if insight_id not in Avalable_Insights:
        return "No data related provided for this insight"
    
    # Extract numeric value from derived_data
    numeric_value = None
    if derived_data:
        first_key = list(derived_data.keys())[0] if derived_data else None
        if first_key:
            value = derived_data[first_key]
            # If it's a dict, get the first numeric value
            if isinstance(value, dict):
                for key, val in value.items():
                    if isinstance(val, (int, float)) and not (isinstance(val, float) and (val != val or val == float('inf'))):
                        numeric_value = float(val)
                        break
            # If it's already a number, use it directly
            elif isinstance(value, (int, float)):
                if hasattr(value, 'item'):
                    numeric_value = value.item()
                else:
                    numeric_value = float(value)
    
    # Get insight config from INSIGHT_MAP
    insight_config = INSIGHT_MAP.get(insight_id, {})
    if not insight_config:
        return "No data related provided for this insight"
    
    insight_details = insight_config.get(insight_name, {})
    if not insight_details:
        return "No data related provided for this insight"
    
    # Map the array based on the numeric value
    if numeric_value is None:
        return "No data related provided for this insight"
    
    if numeric_value > 0:
        array_data = insight_details.get("Goes Up When", set())
        # Convert set to list if needed
        array_list = list(array_data) if isinstance(array_data, set) else array_data
        result = prosses_reasoning_data_and_llm(array_list)
        return result
    elif numeric_value < 0:
        array_data = insight_details.get("Goes Down When", set())
        # Convert set to list if needed
        array_list = list(array_data) if isinstance(array_data, set) else array_data
        result = prosses_reasoning_data_and_llm(array_list)
        return result
    else:  # numeric_value == 0
        zero_reason = insight_details.get("zero because", "No data related provided for this insight")
        return zero_reason

    

    


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
    
    # Get insight ID and name for headline
    insight_id = state.get("mapped_insight_id")
    insight_name = state.get("insight_name")
    
    # Fallback: extract name from INSIGHT_MAP if not in state
    if not insight_name and insight_id:
        insight_dict = INSIGHT_MAP.get(insight_id, {})
        if insight_dict:
            insight_name = list(insight_dict.keys())[0] if insight_dict else "Unknown"
    
    # Create headline
    if insight_id and insight_name:
        headline = f"The input is mapped to insight number {insight_id} which is specialize in {insight_name}"
    else:
        headline = "Analysis result"
    
    print(f"   [Analyst] Generated headline: {headline}")

    analysis = _analyst_analysis(insight_id, insight_name, derived_data)
    print(f"   [Analyst] Generated analysis: {analysis}")
    
    return {
        "final_response": {
            "value": result_value if result_value is not None else 0,
            "headline": headline,
            "analysis": analysis,
            "action_item": "hi",
            "sentiment": "neutral",
            "data": derived_data  # Keep data for debugging
        }
    }



