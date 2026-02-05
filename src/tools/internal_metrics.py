"""
Internal metric tool for fetching company KPIs.

This tool can operate in two modes:
1. Mock mode: Returns hardcoded values (for development)
2. Real mode: Executes SQL queries against BigQuery (for production)

The mode is controlled via environment variables in config/settings.py
"""

from typing import Optional, Any
from .base import BaseInternalTool
from .sql_queries import get_query


class InternalMetricTool(BaseInternalTool):
    """
    Tool for fetching internal metrics from BigQuery or mock data.
    """
    
    def __init__(self, use_mock: bool = True, bigquery_client=None):
        """
        Initialize the internal metric tool.
        
        Args:
            use_mock: If True, use mock data. If False, use BigQuery.
            bigquery_client: BigQuery client instance (required if use_mock=False)
        """
        self.use_mock = use_mock
        self.bigquery_client = bigquery_client
        
        # Mock data for development
        self.mock_db = {
            "internal_arpu": 105.2,
            "internal_revenue": 1500000,
            "internal_latency": 45,        # ms
            "internal_volatility": 12.5,
            "internal_vip_retention": 0.94,  # 94%
            "internal_churn": 0.04,        # 4%
        }
    
    def fetch_metric(self, metric_key: str) -> Optional[Any]:
        """
        Fetch an internal metric by key.
        
        Args:
            metric_key: The metric identifier (e.g., "internal_revenue")
            
        Returns:
            The metric value, or None if not found
        """
        if self.use_mock:
            return self._fetch_mock(metric_key)
        else:
            return self._fetch_bigquery(metric_key)
    
    def _fetch_mock(self, metric_key: str) -> Optional[Any]:
        """Fetch metric from mock data."""
        print(f"   [Tool: SQL (MOCK)] Fetching '{metric_key}'...")
        return self.mock_db.get(metric_key)
    
    def _fetch_bigquery(self, metric_key: str) -> Optional[Any]:
        """
        Fetch metric from BigQuery.
        
        This method will be implemented when integrating with real BigQuery.
        """
        if not self.bigquery_client:
            raise ValueError("BigQuery client is required for real mode")
        
        query = get_query(metric_key)
        if not query:
            print(f"   [Tool: SQL] No query found for '{metric_key}'")
            return None
        
        print(f"   [Tool: SQL (BigQuery)] Executing query for '{metric_key}'...")
        
        # TODO: Implement actual BigQuery execution
        # Example:
        # query_job = self.bigquery_client.query(query)
        # results = query_job.result()
        # return results[0][0] if results else None
        
        # For now, return None to indicate not implemented
        print(f"   [Tool: SQL] BigQuery integration not yet implemented")
        return None


# Global instance (will be initialized in config/settings.py)
_internal_tool_instance: Optional[InternalMetricTool] = None


def get_internal_tool() -> InternalMetricTool:
    """
    Get the global internal metric tool instance.
    
    Returns:
        The InternalMetricTool instance
    """
    global _internal_tool_instance
    if _internal_tool_instance is None:
        # Default to mock mode. Will be configured properly in settings
        _internal_tool_instance = InternalMetricTool(use_mock=True)
    return _internal_tool_instance
