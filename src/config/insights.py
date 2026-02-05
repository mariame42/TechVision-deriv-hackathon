"""
Insight ID mappings (1-18).

This module maps Insight IDs to their names and required metrics.
Used by the classifier node to determine which metrics to fetch.
"""

from typing import Dict, List

# Map of Insight ID to insight information
INSIGHT_MAP: Dict[int, Dict[str, any]] = {
    1: {
        "name": "General Trend Analysis",
        "required_metrics": ["internal_revenue", "internal_arpu"],
    },
    
    17: {
        "name": "Revenue Drop Root Cause",
        "required_metrics": [
            "internal_revenue",
            "internal_latency",
            "internal_volatility",
            "external_btc_price",
            "external_market_volatility",
        ],
    },
    
    # TODO: Add remaining insights (2-16, 18)
    # Example structure:
    # 2: {
    #     "name": "VIP Retention Analysis",
    #     "required_metrics": ["internal_vip_retention", "internal_churn"],
    # },
}

