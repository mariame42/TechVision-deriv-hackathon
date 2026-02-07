#!/usr/bin/env python3
"""
Quick test script to see the enhanced classifier logging.
Run this locally (no Docker needed) to see the decision process.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.state import AgentState
from src.nodes.classifier import node_classifier

def test_classifier_with_logging():
    """Test classifier with detailed logging output."""
    
    print("\n" + "="*70)
    print("TESTING CLASSIFIER WITH ENHANCED LOGGING")
    print("="*70 + "\n")
    
    test_queries = [
        "Why did we lose money?",
        "How is our volatility compared to the market?",
        "What about our active traders?",
        "Check VIP migration status",
        "Why is latency so high?",
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'='*70}")
        print(f"TEST {i}: '{query}'")
        print('='*70 + "\n")
        
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
        
        # Call classifier (will show all the detailed logs)
        result = node_classifier(test_state)
        
        print(f"\n{'─'*70}")
        print("FINAL RESULT:")
        print(f"  Insight ID: {result.get('mapped_insight_id')}")
        print(f"  Insight Name: {result.get('insight_name')}")
        print(f"  Required Metrics: {result.get('required_metrics')}")
        print('─'*70)
    
    print(f"\n{'='*70}")
    print("TEST COMPLETE")
    print("="*70)
    print("\nTo see LLM classification, set OPENROUTER_API_KEY:")
    print("  export OPENROUTER_API_KEY=sk-or-v1-your-key-here")
    print("="*70 + "\n")

if __name__ == "__main__":
    test_classifier_with_logging()

