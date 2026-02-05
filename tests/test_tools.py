"""
Tests for data fetching tools.
"""

import pytest
from src.tools import get_internal_tool, get_external_tool


def test_internal_tool_mock():
    """Test internal tool with mock data."""
    tool = get_internal_tool()
    result = tool.fetch_metric("internal_revenue")
    assert result is not None
    assert isinstance(result, (int, float))


def test_external_tool_mock():
    """Test external tool with mock data."""
    tool = get_external_tool()
    result = tool.fetch_metric("external_btc_price")
    assert result is not None
    assert isinstance(result, (int, float))

