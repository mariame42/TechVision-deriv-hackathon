"""
Configuration management for the application.
"""

from .settings import Settings, get_settings
from .insights import INSIGHT_MAP

__all__ = ["Settings", "get_settings", "INSIGHT_MAP"]

