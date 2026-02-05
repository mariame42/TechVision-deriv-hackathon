"""
SQL query definitions for BigQuery.

This module contains all SQL queries mapped to metric keys.
When switching to real BigQuery, these queries will be executed directly.
"""

from .metric_queries import METRIC_QUERY_MAP, get_query

__all__ = ["METRIC_QUERY_MAP", "get_query"]
