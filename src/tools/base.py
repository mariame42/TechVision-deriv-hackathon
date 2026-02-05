"""
Abstract base classes for tools.

This provides an abstraction layer to easily switch between
mock implementations (for development) and real implementations
(for production with BigQuery and external APIs).
"""

from abc import ABC, abstractmethod
from typing import Optional, Any


class BaseInternalTool(ABC):
    """
    Abstract base class for internal metric tools.
    
    Implementations can use mock data or real BigQuery queries.
    """
    
    @abstractmethod
    def fetch_metric(self, metric_key: str) -> Optional[Any]:
        """
        Fetch an internal metric by key.
        
        Args:
            metric_key: The metric identifier (e.g., "internal_revenue")
            
        Returns:
            The metric value, or None if not found
        """
        pass


class BaseExternalTool(ABC):
    """
    Abstract base class for external API tools.
    
    Implementations can use mock data or real API calls.
    """
    
    @abstractmethod
    def fetch_metric(self, metric_key: str) -> Optional[Any]:
        """
        Fetch an external metric by key.
        
        Args:
            metric_key: The metric identifier (e.g., "external_btc_price")
            
        Returns:
            The metric value, or None if not found
        """
        pass
