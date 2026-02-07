"""
Node C: Intent Classifier (Chat Path)

Maps user questions to Insight IDs (1-18) and determines required metrics.
Uses LLM to understand user intent and route to appropriate analysis.
"""

import json
from typing import Optional
from ..state import AgentState
from ..config.insights import INSIGHT_MAP
from ..config.settings import get_settings


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
    
    if not query:
        print("   [Classifier] WARNING: No user_query found in state!")
        return {
            "mapped_insight_id": 1,
            "insight_name": "General Analysis",
            "required_metrics": [],
        }
    
    settings = get_settings()
    
    print(f"   [Classifier] ───────────────────────────────────────────────────────────")
    print(f"   [Classifier] Classification Method Selection:")
    
    # Use LLM if OpenRouter API key is configured, otherwise fall back to simple matching
    if settings.openrouter_api_key:
        print(f"   [Classifier] ✓ OpenRouter API key: CONFIGURED")
        print(f"   [Classifier] → Method: LLM-based classification")
        print(f"   [Classifier] → Model: {settings.llm_model or 'openai/gpt-3.5-turbo'}")
        print(f"   [Classifier] ───────────────────────────────────────────────────────────")
        try:
            insight_id = _classify_intent_llm(query, settings)
            print(f"   [Classifier] ✓ LLM classification successful: Insight {insight_id}")
        except Exception as e:
            print(f"   [Classifier] ✗ LLM classification failed: {e}")
            print(f"   [Classifier] → Falling back to simple keyword matching")
            print(f"   [Classifier] ───────────────────────────────────────────────────────────")
            insight_id = _classify_intent_simple(query)
    else:
        print(f"   [Classifier] ✗ OpenRouter API key: NOT CONFIGURED")
        print(f"   [Classifier] → Method: Simple keyword matching (fallback mode)")
        print(f"   [Classifier] → To enable LLM, set OPENROUTER_API_KEY environment variable")
        print(f"   [Classifier] ───────────────────────────────────────────────────────────")
        # Fallback to simple keyword matching
        insight_id = _classify_intent_simple(query)
    
    insight_info = INSIGHT_MAP.get(insight_id, {})
    
    # Handle the insight info structure (it might have nested structure)
    if isinstance(insight_info, dict) and insight_info:
        # Get the first key as name if structure is nested like {1: {"Trading revenue change": {...}}}
        first_key = list(insight_info.keys())[0]
        if isinstance(insight_info[first_key], dict) and "required_metrics" in insight_info[first_key]:
            # Nested structure: {1: {"Trading revenue change": {"required_metrics": [...]}}}
            name = first_key
            required_metrics = insight_info[first_key].get("required_metrics", [])
        elif "required_metrics" in insight_info:
            # Flat structure: {1: {"name": "...", "required_metrics": [...]}}
            name = insight_info.get("name", first_key)
            required_metrics = insight_info.get("required_metrics", [])
        else:
            name = first_key
            required_metrics = []
    else:
        name = "General Analysis"
        required_metrics = []
    
    result_state = {
        "mapped_insight_id": insight_id,
        "insight_name": name,
        "required_metrics": required_metrics,
    }
    
    print(f"   [Classifier] Returning state update:")
    print(f"   [Classifier]   - mapped_insight_id: {insight_id}")
    print(f"   [Classifier]   - insight_name: {name}")
    print(f"   [Classifier]   - required_metrics: {required_metrics}")
    
    return result_state


def _classify_intent_llm(query: str, settings) -> int:
    """
    Classify user intent using OpenRouter LLM API.
    
    Args:
        query: User's question
        settings: Application settings
        
    Returns:
        Insight ID (1-18)
    """
    try:
        from openai import OpenAI
        
        # Initialize OpenAI client with OpenRouter endpoint
        client = OpenAI(
            api_key=settings.openrouter_api_key,
            base_url=settings.openrouter_base_url,
        )
        
        # Build the prompt with all available insights
        insights_list = []
        for insight_id, insight_data in INSIGHT_MAP.items():
            if isinstance(insight_data, dict) and insight_data:
                # Handle nested structure: {1: {"Trading revenue change": {...}}}
                first_key = list(insight_data.keys())[0]
                if isinstance(insight_data[first_key], dict):
                    name = first_key
                else:
                    name = insight_data.get("name", first_key)
                insights_list.append(f"{insight_id}. {name}")
            else:
                insights_list.append(f"{insight_id}. Insight {insight_id}")
        
        insights_text = "\n".join(insights_list)
        
        system_prompt = f"""You are an AI classifier for a trading analytics platform. 
Your task is to analyze user questions and map them to one of the following insights:

{insights_text}

Analyze the user's question and return ONLY a JSON object with this exact structure:
{{"insight_id": <number between 1-18>, "confidence": <0.0-1.0>, "reasoning": "<brief explanation>"}}

Choose the insight ID that best matches the user's intent. If unsure, default to insight ID 1."""

        user_prompt = f"User question: {query}\n\nReturn the JSON classification:"

        # Use a valid OpenRouter model ID
        model_id = settings.llm_model or "openai/gpt-3.5-turbo"
        
        # If model doesn't have provider prefix, try to detect the correct provider
        # OpenRouter requires format: "provider/model" (e.g., "openai/gpt-3.5-turbo")
        if "/" not in model_id:
            print(f"   [Classifier] WARNING: Model '{model_id}' missing provider prefix")
            
            # Smart detection based on model name
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
                # Default to OpenAI for unknown models
                provider = "openai"
            
            model_id = f"{provider}/{model_id}"
            print(f"   [Classifier] → Converting to OpenRouter format: '{model_id}'")
        
        print(f"   [Classifier] Sending request to OpenRouter API...")
        print(f"   [Classifier] Model: {model_id}")
        print(f"   [Classifier] User query: '{query}'")
        
        # Call OpenRouter API
        response = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,  # Lower temperature for more consistent classification
            response_format={"type": "json_object"},  # Force JSON output
        )
        
        print(f"   [Classifier] Received response from LLM")
        
        # Parse the response
        content = response.choices[0].message.content
        print(f"   [Classifier] Raw LLM response: {content}")
        result = json.loads(content)
        print(f"   [Classifier] Parsed JSON: {result}")
        
        insight_id = result.get("insight_id", 1)
        confidence = result.get("confidence", 0.0)
        reasoning = result.get("reasoning", "")
        
        print(f"   [Classifier] LLM classified as Insight {insight_id} (confidence: {confidence:.2f})")
        if reasoning:
            print(f"   [Classifier] Reasoning: {reasoning}")
        
        # Validate insight_id is in range
        if not (1 <= insight_id <= 18):
            print(f"   [Classifier] Invalid insight_id {insight_id}, defaulting to 1")
            insight_id = 1
        
        return insight_id
        
    except json.JSONDecodeError as e:
        print(f"   [Classifier] Failed to parse LLM JSON response: {e}")
        return _classify_intent_simple(query)
    except Exception as e:
        print(f"   [Classifier] LLM classification error: {e}")
        raise


def _classify_intent_simple(query: str) -> int:
    """
    Simple keyword-based classification (fallback when LLM is not available).
    
    Args:
        query: User's question
        
    Returns:
        Insight ID (1-18)
    """
    query_lower = query.lower()
    print(f"   [Classifier] Using simple keyword matching for: '{query}'")
    print(f"   [Classifier] Analyzing query for keyword patterns...")
    
    # Define keyword patterns with their insight IDs and descriptions
    keyword_patterns = [
        {
            "insight_id": 17,
            "name": "Revenue drop root cause chain",
            "keywords": ["lose", "lost", "money", "revenue", "drop", "down", "decrease", "decline", "fall"],
            "reasoning": "Keywords related to revenue loss or decrease"
        },
        {
            "insight_id": 7,
            "name": "Volatility regime shift",
            "keywords": ["volatility", "volatile", "vol", "volatile", "market volatility"],
            "reasoning": "Keywords related to market volatility"
        },
        {
            "insight_id": 4,
            "name": "Active trader change",
            "keywords": ["trader", "traders", "active", "trading activity", "user activity"],
            "reasoning": "Keywords related to trader activity"
        },
        {
            "insight_id": 5,
            "name": "VIP migration",
            "keywords": ["vip", "migration", "premium", "high value"],
            "reasoning": "Keywords related to VIP customers"
        },
        {
            "insight_id": 10,
            "name": "Exposure concentration",
            "keywords": ["risk", "exposure", "concentration", "portfolio risk"],
            "reasoning": "Keywords related to risk exposure"
        },
        {
            "insight_id": 11,
            "name": "Leverage spike",
            "keywords": ["leverage", "leverage ratio", "margin"],
            "reasoning": "Keywords related to leverage"
        },
        {
            "insight_id": 12,
            "name": "Margin call acceleration",
            "keywords": ["margin call", "margin", "liquidation"],
            "reasoning": "Keywords related to margin calls"
        },
        {
            "insight_id": 13,
            "name": "Latency impact",
            "keywords": ["latency", "speed", "slow", "delay", "response time", "performance"],
            "reasoning": "Keywords related to system performance/latency"
        },
        {
            "insight_id": 14,
            "name": "Order rejection spike",
            "keywords": ["reject", "rejection", "order", "failed order", "order failure"],
            "reasoning": "Keywords related to order rejections"
        },
        {
            "insight_id": 1,
            "name": "Trading revenue change",
            "keywords": ["revenue", "income", "earnings", "profit"],
            "reasoning": "General revenue-related keywords"
        },
    ]
    
    # Check each pattern
    matched_patterns = []
    for pattern in keyword_patterns:
        matched_keywords = [kw for kw in pattern["keywords"] if kw in query_lower]
        if matched_keywords:
            matched_patterns.append({
                "insight_id": pattern["insight_id"],
                "name": pattern["name"],
                "matched_keywords": matched_keywords,
                "reasoning": pattern["reasoning"]
            })
    
    # Log all matches found
    if matched_patterns:
        print(f"   [Classifier] ✓ Found {len(matched_patterns)} matching pattern(s):")
        for i, match in enumerate(matched_patterns, 1):
            print(f"   [Classifier]   [{i}] Insight {match['insight_id']}: {match['name']}")
            print(f"   [Classifier]       └─ Matched keywords: {', '.join(match['matched_keywords'])}")
            print(f"   [Classifier]       └─ Reasoning: {match['reasoning']}")
        
        # Return the first (highest priority) match
        selected = matched_patterns[0]
        print(f"   [Classifier]")
        print(f"   [Classifier] ════════════════════════════════════════════════════════")
        print(f"   [Classifier] DECISION: Selected Insight {selected['insight_id']}")
        print(f"   [Classifier] Name: {selected['name']}")
        print(f"   [Classifier] Matched Keywords: {', '.join(selected['matched_keywords'])}")
        print(f"   [Classifier] Reasoning: {selected['reasoning']}")
        print(f"   [Classifier] ════════════════════════════════════════════════════════")
        return selected["insight_id"]
    else:
        print(f"   [Classifier] ✗ No keyword patterns matched in query: '{query}'")
        print(f"   [Classifier]   Available patterns checked: {len(keyword_patterns)}")
        print(f"   [Classifier] ════════════════════════════════════════════════════════")
        print(f"   [Classifier] DECISION: Defaulting to Insight 1 (General Analysis)")
        print(f"   [Classifier] ════════════════════════════════════════════════════════")
        return 1  # Default to general analysis
