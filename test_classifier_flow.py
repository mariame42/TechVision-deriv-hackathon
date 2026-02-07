"""
Test script to verify the classifier flow is working correctly.

This script tests:
1. Classifier receives user_query from state
2. Checks for OpenRouter API key
3. Calls LLM (or falls back to simple matching)
4. Returns correct insight_id, insight_name, and required_metrics
"""

import os
from src.state import AgentState
from src.nodes.classifier import node_classifier

def test_classifier_flow():
    """Test the complete classifier flow."""
    
    print("=" * 60)
    print("TESTING CLASSIFIER FLOW")
    print("=" * 60)
    
    # Test 1: Check if OpenRouter API key is set
    settings = __import__('src.config.settings', fromlist=['get_settings']).get_settings()
    has_api_key = bool(settings.openrouter_api_key)
    print(f"\n1. OpenRouter API Key Status: {'✓ SET' if has_api_key else '✗ NOT SET (will use simple matching)'}")
    
    # Test 2: Test with a sample query
    test_queries = [
        "Why did we lose money today?",
        "How is our volatility compared to the market?",
        "What is our current revenue trend?",
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'=' * 60}")
        print(f"TEST {i}: Query = '{query}'")
        print('=' * 60)
        
        # Create test state
        test_state: AgentState = {
            "request_type": "chat_query",
            "chat_history": [],
            "user_query": query,
            "target_domain": None,
            "mapped_insight_id": None,
            "insight_name": None,
            "required_metrics": [],
            "fetched_data": {},
            "derived_data": {},
            "root_cause_analysis": None,
            "final_response": {},
            "errors": [],
        }
        
        # Call classifier
        try:
            result = node_classifier(test_state)
            
            # Verify results
            print(f"\n✓ Classifier executed successfully")
            print(f"  - mapped_insight_id: {result.get('mapped_insight_id')}")
            print(f"  - insight_name: {result.get('insight_name')}")
            print(f"  - required_metrics: {result.get('required_metrics')}")
            
            # Validate
            insight_id = result.get('mapped_insight_id')
            if not insight_id or not (1 <= insight_id <= 18):
                print(f"  ✗ ERROR: Invalid insight_id: {insight_id}")
            else:
                print(f"  ✓ Valid insight_id: {insight_id}")
            
            if not result.get('insight_name'):
                print(f"  ✗ ERROR: Missing insight_name")
            else:
                print(f"  ✓ insight_name present: {result.get('insight_name')}")
            
            if not isinstance(result.get('required_metrics'), list):
                print(f"  ✗ ERROR: required_metrics is not a list")
            else:
                print(f"  ✓ required_metrics is a list with {len(result.get('required_metrics', []))} items")
                
        except Exception as e:
            print(f"\n✗ ERROR: Classifier failed with exception: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'=' * 60}")
    print("TEST SUMMARY")
    print('=' * 60)
    print(f"OpenRouter API Key: {'Configured' if has_api_key else 'Not Configured'}")
    print(f"To enable LLM classification, set OPENROUTER_API_KEY in your environment")
    print("=" * 60)


if __name__ == "__main__":
    test_classifier_flow()

