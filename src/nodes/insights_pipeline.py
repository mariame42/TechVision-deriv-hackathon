"""
Node: Insights Pipeline (Replaces Node D + Node E)

Unified pipeline that:
1. Fetches data from PostgreSQL
2. Preprocesses and cleans data
3. Computes insights using InsightsEngine
4. Returns results in LangGraph state format

This replaces:
- Node D (Hybrid Fetcher) - no longer needed
- Node E (Math Engine) - logic moved to InsightsEngine
"""

import logging
import os
from typing import Dict, Any
from ..state import AgentState
from ..db import get_connection
from ..preprocessing import DataPreprocessor
from ..insights import InsightsEngine

logger = logging.getLogger(__name__)


def node_insights_pipeline(state: AgentState) -> AgentState:
    """
    Unified pipeline: Fetch from PostgreSQL → Compute insights → Return results.
    
    Replaces Node D (Hybrid Fetcher) + Node E (Math Engine).
    
    Args:
        state: The current agent state with mapped_insight_id
        
    Returns:
        Updated state with derived_data (computed insights)
    """
    insight_id = state.get("mapped_insight_id")
    insight_name = state.get("insight_name", "Unknown")
    
    print(f"--- INSIGHTS PIPELINE: Computing Insight #{insight_id} ({insight_name}) ---")
    
    errors = state.get("errors", []).copy()
    derived_data = {}
    
    if not insight_id:
        error_msg = "No insight_id found in state"
        logger.warning(error_msg)
        errors.append(error_msg)
        return {
            "fetched_data": {},
            "derived_data": {},
            "errors": errors
        }
    
    # Map insight_id to InsightsEngine method
    insight_method_map = {
        1: "trading_revenue_change",
        3: "revenue_sensitivity_to_volatility",
        4: "active_trader_change",
        7: "volatility_regime_shift",
        8: "volume_contraction",
        9: "asset_rotation_detection",
        17: "revenue_drop_root_cause",
    }
    
    method_name = insight_method_map.get(insight_id)
    
    if not method_name:
        error_msg = f"No InsightsEngine method found for insight_id {insight_id}"
        logger.warning(error_msg)
        errors.append(error_msg)
        return {
            "fetched_data": {},
            "derived_data": {},
            "errors": errors
        }
    
    # Initialize pipeline components
    conn = None
    try:
        # 1. Get PostgreSQL connection
        print(f"   [Pipeline] Connecting to PostgreSQL...")
        print(f"   [Pipeline] Host: {os.getenv('POSTGRES_HOST', 'not set')}")
        print(f"   [Pipeline] Database: {os.getenv('POSTGRES_DATABASE', 'not set')}")
        conn = get_connection()
        print(f"   [Pipeline] ✓ PostgreSQL connection established")
        
        # 2. Initialize preprocessor
        preprocessor = DataPreprocessor(conn)
        
        # 3. Initialize insights engine
        engine = InsightsEngine(preprocessor)
        
        # 4. Execute insight computation
        print(f"   [Pipeline] Computing {method_name}...")
        method = getattr(engine, method_name)
        result = method()
        
        print(f"   [Pipeline] Raw result from {method_name}: {result} (type: {type(result).__name__})")
        
        # 5. Format result for LangGraph state
        derived_data = _format_insight_result(insight_id, method_name, result)
        
        print(f"   [Pipeline] ✓ Insight computed successfully")
        print(f"   [Pipeline] Formatted result: {derived_data}")
        
    except Exception as e:
        error_msg = f"Pipeline execution failed: {str(e)}"
        logger.error(error_msg, exc_info=True)
        errors.append(error_msg)
        print(f"   [Pipeline] ✗ Error: {error_msg}")
        import traceback
        traceback.print_exc()
        
    finally:
        # 6. Cleanup: Close connection
        if conn:
            try:
                conn.close()
                print(f"   [Pipeline] Database connection closed")
            except Exception as e:
                logger.warning(f"Error closing connection: {e}")
    
    return {
        "fetched_data": {},  # Empty - all data computed internally
        "derived_data": derived_data,
        "errors": errors
    }


def _format_insight_result(insight_id: int, method_name: str, result: Any) -> Dict[str, Any]:
    """
    Format InsightsEngine result for LangGraph state.
    
    Maps method results to derived_data keys that Analyst expects.
    
    Args:
        insight_id: The insight ID
        method_name: Name of the method that was called
        result: Raw result from InsightsEngine method
        
    Returns:
        Dictionary formatted for derived_data
    """
    # For single-value results, use method name as key
    if isinstance(result, (int, float)):
        return {method_name: result}
    
    # For dict results (like revenue_drop_root_cause), return as-is
    if isinstance(result, dict):
        return result
    
    # For empty results, return empty dict
    if result is None:
        return {}
    
    # Fallback: wrap in dict with method name
    return {method_name: result}

