"""
SQL query mappings for internal metrics.

This module maps metric keys to their corresponding BigQuery SQL queries.
In production, these queries will be executed against BigQuery.

Note: These are example queries. Replace with your actual table names
and column names when integrating with real BigQuery.
"""

from typing import Dict, Optional

# Map of metric keys to SQL queries
METRIC_QUERY_MAP: Dict[str, str] = {
    "internal_arpu": """
        SELECT 
            SUM(revenue) / COUNT(DISTINCT active_users) as arpu
        FROM metrics_daily
        WHERE date = CURRENT_DATE()
    """,
    
    "internal_revenue": """
        SELECT 
            SUM(total_revenue) as revenue
        FROM finance_gold
        WHERE date = CURRENT_DATE()
    """,
    
    "internal_latency": """
        SELECT 
            AVG(execution_time_ms) as avg_latency
        FROM tech_logs
        WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR)
    """,
    
    "internal_volatility": """
        SELECT 
            STDDEV(price_change) as volatility
        FROM trading_metrics
        WHERE date = CURRENT_DATE()
    """,
    
    "internal_vip_retention": """
        SELECT 
            COUNT(DISTINCT retained_vip_users) / COUNT(DISTINCT total_vip_users) as retention_rate
        FROM metrics_monthly
        WHERE month = DATE_TRUNC(CURRENT_DATE(), MONTH)
    """,
    
    "internal_churn": """
        SELECT 
            COUNT(lost_users) / COUNT(total_users) as churn_rate
        FROM metrics_monthly
        WHERE month = DATE_TRUNC(CURRENT_DATE(), MONTH)
    """,
}


def get_query(metric_key: str) -> Optional[str]:
    """
    Get the SQL query for a given metric key.
    
    Args:
        metric_key: The metric identifier
        
    Returns:
        The SQL query string, or None if not found
    """
    return METRIC_QUERY_MAP.get(metric_key)
