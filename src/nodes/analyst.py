"""
Node F: The Analyst (Root Cause Engine)

Generates the JSON narrative using Raw + Derived Data.
Uses LLM to create human-readable insights from the collected data.
"""

import json
import random
from typing import Optional
from ..state import AgentState
from ..config.insights import INSIGHT_MAP
from ..config.settings import get_settings

def genarate_with_LLM(array_of_data: list) -> str:
    """
    Generate analysis text using LLM based on randomly selected reasons from the array.
    
    Randomly selects 2 items from the array and uses LLM to create a natural explanation
    that connects these reasons together.
    
    Args:
        array_of_data: List or set of possible reasons (e.g., ["More trades", "Higher fees", ...])
        
    Returns:
        Generated analysis text explaining the reason
    """
    if not array_of_data or len(array_of_data) == 0:
        return "No data available for analysis"
    
    # Ensure array_of_data is a list (convert set to list if needed)
    if isinstance(array_of_data, set):
        array_of_data = list(array_of_data)
    elif not isinstance(array_of_data, (list, tuple)):
        # If it's not a list, tuple, or set, try to convert
        try:
            array_of_data = list(array_of_data)
        except (TypeError, ValueError):
            return "Invalid data format for analysis"
    
    # Randomly select 2 items from the array
    # If array has less than 2 items, use all available items
    num_to_select = min(2, len(array_of_data))
    selected_reasons = random.sample(array_of_data, num_to_select)
    
    print(f"   [Analyst] Selected {num_to_select} reason(s) from {len(array_of_data)} available:")
    for i, reason in enumerate(selected_reasons, 1):
        print(f"   [Analyst]   [{i}] {reason}")
    
    # Get settings for LLM
    settings = get_settings()
    
    # Check if OpenRouter API key is configured
    if not settings.openrouter_api_key:
        print(f"   [Analyst] WARNING: OpenRouter API key not configured, returning simple explanation")
        # Fallback: simple concatenation
        return f"The main reasons are: {', '.join(selected_reasons)}."
    
    try:
        from openai import OpenAI
        
        # Initialize OpenAI client with OpenRouter endpoint
        client = OpenAI(
            api_key=settings.openrouter_api_key,
            base_url=settings.openrouter_base_url,
        )
        
        # Prepare the selected reasons as a formatted list
        reasons_text = "\n".join([f"- {reason}" for reason in selected_reasons])
        
        # Create a prompt that asks the LLM to generate a natural explanation
        system_prompt = """You are an AI analyst for a trading analytics platform. 
Your task is to generate a clear, professional explanation that connects multiple business reasons together.

Write a concise, natural-sounding explanation (2-3 sentences) that explains how these reasons relate to each other and contribute to the observed metric change. 
Use professional trading/financial terminology and make it sound like a real analyst's insight.

Example format:
"The primary driver is [reason 1], which has opened opportunities for [reason 2]. This combination has led to [outcome]."

Keep it professional, clear, and focused on business impact."""
        
        user_prompt = f"""Based on the following reasons, generate a natural explanation that connects them:

{reasons_text}

Generate a professional analysis explaining how these factors contribute to the observed change:"""
        
        # Use the same model as classifier
        model_id = settings.llm_model or "openai/gpt-3.5-turbo"
        
        # Handle model ID format (same logic as classifier)
        if "/" not in model_id:
            model_lower = model_id.lower()
            if "gemini" in model_lower:
                provider = "google"
            elif "claude" in model_lower or "anthropic" in model_lower:
                provider = "anthropic"
            elif "llama" in model_lower or "meta" in model_lower:
                provider = "meta-llama"
            elif "gpt" in model_lower or "turbo" in model_lower:
                provider = "openai"
            else:
                provider = "openai"
            model_id = f"{provider}/{model_id}"
        
        print(f"   [Analyst] Calling LLM to generate analysis...")
        print(f"   [Analyst] Model: {model_id}")
        
        # Call OpenRouter API
        response = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,  # Slightly higher temperature for more natural language
            max_tokens=150,   # Limit to keep responses concise
        )
        
        # Extract the generated text
        generated_text = response.choices[0].message.content.strip()
        print(f"   [Analyst] ✓ LLM generated analysis: {generated_text}")
        
        return generated_text
        
    except Exception as e:
        print(f"   [Analyst] ✗ LLM generation failed: {e}")
        print(f"   [Analyst] → Falling back to simple explanation")
        # Fallback: simple concatenation
        return f"The main reasons are: {', '.join(selected_reasons)}."

def prosses_reasoning_data_and_llm(array_of_data: list) -> str:
    """
    Process reasoning data and generate LLM response.
    
    Args:
        array_of_data: List of possible reasons
        
    Returns:
        Generated analysis text from LLM
    """
    if not array_of_data or len(array_of_data) == 0:
        return "The reason is not found in the data base"
    
    return genarate_with_LLM(array_of_data)


def _analyst_analysis(insight_id: Optional[int], insight_name: Optional[str], derived_data: dict) -> str:
    """
    Generate analysis text based on insight ID and name.
    
    Args:
        insight_id: The insight ID (can be None)
        insight_name: The insight name (can be None)
        derived_data: The derived data dict
    """
    # Validate inputs
    if insight_id is None:
        return "No insight ID provided"
    
    Avalable_Insights = {1, 3, 4, 8, 9}
    if insight_id not in Avalable_Insights:
        return "No data related provided for this insight"
    
    # Extract numeric value from derived_data
    numeric_value = None
    if derived_data and isinstance(derived_data, dict):
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
    
    # If insight_name is None, try to get the first key from insight_config
    if not insight_name:
        if insight_config and isinstance(insight_config, dict):
            insight_name = list(insight_config.keys())[0] if insight_config else None
        if not insight_name:
            return "No insight name provided"
    
    insight_details = insight_config.get(insight_name, {})
    if not insight_details:
        return "No data related provided for this insight"
    
    # Map the array based on the numeric value
    if numeric_value is None:
        return "No data related provided for this insight"
    
    if numeric_value > 0:
        array_data = insight_details.get("Goes Up When", set())
        # Convert set to list if needed, ensure it's a list
        if isinstance(array_data, set):
            array_list = list(array_data)
        elif isinstance(array_data, (list, tuple)):
            array_list = list(array_data)
        else:
            # If it's not a set, list, or tuple, return error
            return "Invalid data format for 'Goes Up When'"
        result = prosses_reasoning_data_and_llm(array_list)
        return result
    elif numeric_value < 0:
        array_data = insight_details.get("Goes Down When", set())
        # Convert set to list if needed, ensure it's a list
        if isinstance(array_data, set):
            array_list = list(array_data)
        elif isinstance(array_data, (list, tuple)):
            array_list = list(array_data)
        else:
            # If it's not a set, list, or tuple, return error
            return "Invalid data format for 'Goes Down When'"
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
    
    if derived_data and isinstance(derived_data, dict):
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
            "action_item": ".",
            "sentiment": "neutral",
            "data": derived_data  # Keep data for debugging
        }
    }



