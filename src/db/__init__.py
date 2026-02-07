"""Database connection module."""

from .postgres_connector import get_connection

__all__ = ["get_connection"]

