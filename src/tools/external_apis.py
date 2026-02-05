"""
External market API tool for fetching market data.

This tool can operate in two modes:
1. Mock mode: Returns hardcoded values (for development)
2. Real mode: Makes actual HTTP requests to external APIs (for production)

The mode is controlled via environment variables in config/settings.py
"""

from typing import Optional, Any
import requests
from .base import BaseExternalTool


class ExternalMarketTool(BaseExternalTool):
    """
    Tool for fetching external market data from APIs or mock data.
    """
    
    def __init__(self, use_mock: bool = True):
        """
        Initialize the external market tool.
        
        Args:
            use_mock: If True, use mock data. If False, make real API calls.
        """
        self.use_mock = use_mock
        
        # API endpoint mappings
        self.api_map = {
            "external_btc_price": "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd",
            "external_volatility_vix": "https://api.bloomberg.com/vix",  # Example endpoint
            "external_competitor_rate": "https://competitor-scraper/rates",  # Example endpoint
            "external_market_volatility": "https://api.marketdata.com/volatility",  # Example endpoint
        }
        
        # Mock data for development
        self.mock_api = {
            "external_btc_price": 64500.00,
            "external_volatility_vix": 18.5,
            "external_competitor_rate": 0.02,
            "external_market_volatility": 18.5,
        }
    
    def fetch_metric(self, metric_key: str) -> Optional[Any]:
        """
        Fetch an external metric by key.
        
        Args:
            metric_key: The metric identifier (e.g., "external_btc_price")
            
        Returns:
            The metric value, or None if not found
        """
        if self.use_mock:
            return self._fetch_mock(metric_key)
        else:
            return self._fetch_api(metric_key)
    
    def _fetch_mock(self, metric_key: str) -> Optional[Any]:
        """Fetch metric from mock data."""
        print(f"   [Tool: API (MOCK)] Fetching '{metric_key}'...")
        return self.mock_api.get(metric_key)
    
    def _fetch_api(self, metric_key: str) -> Optional[Any]:
        """
        Fetch metric from external API.
        
        This method makes actual HTTP requests to external APIs.
        """
        if metric_key not in self.api_map:
            print(f"   [Tool: API] No endpoint found for '{metric_key}'")
            return None
        
        endpoint = self.api_map[metric_key]
        print(f"   [Tool: API] Calling {endpoint}...")
        
        try:
            # TODO: Implement actual API calls with proper error handling
            # Example:
            # response = requests.get(endpoint, timeout=5)
            # response.raise_for_status()
            # data = response.json()
            # return self._parse_response(metric_key, data)
            
            # For now, return None to indicate not implemented
            print(f"   [Tool: API] Real API integration not yet implemented")
            return None
            
        except Exception as e:
            print(f"   [Tool: API] Error fetching {metric_key}: {str(e)}")
            return None
    
    def _parse_response(self, metric_key: str, data: dict) -> Optional[Any]:
        """
        Parse API response based on metric key.
        
        Different APIs return different formats, so we need to parse accordingly.
        """
        # Example parsing logic (customize based on actual API responses)
        if metric_key == "external_btc_price":
            return data.get("bitcoin", {}).get("usd")
        elif metric_key == "external_volatility_vix":
            return data.get("vix")
        # Add more parsing logic as needed
        return None


# Global instance (will be initialized in config/settings.py)
_external_tool_instance: Optional[ExternalMarketTool] = None


def get_external_tool() -> ExternalMarketTool:
    """
    Get the global external market tool instance.
    
    Returns:
        The ExternalMarketTool instance
    """
    global _external_tool_instance
    if _external_tool_instance is None:
        # Default to mock mode. Will be configured properly in settings
        _external_tool_instance = ExternalMarketTool(use_mock=True)
    return _external_tool_instance
