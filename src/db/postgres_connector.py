"""
PostgreSQL database connector.

Provides centralized database connection management.
This is the ONLY database entry point for the pipeline.
"""

import psycopg2
import logging
from typing import Optional
from ..config.settings import get_settings

logger = logging.getLogger(__name__)


def get_connection():
    """
    Connect to PostgreSQL database.
    
    Uses settings from environment variables:
    - POSTGRES_HOST (default: localhost)
    - POSTGRES_DATABASE (default: trading_db)
    - POSTGRES_USER (default: postgres)
    - POSTGRES_PASSWORD (required)
    - POSTGRES_PORT (default: 5432)
    
    Returns:
        psycopg2.connection: Database connection object
        
    Raises:
        Exception: If connection fails
    """
    settings = get_settings()
    
    # Validate required settings
    if not settings.postgres_password:
        error_msg = "POSTGRES_PASSWORD environment variable is required but not set"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    try:
        conn = psycopg2.connect(
            host=settings.postgres_host,
            database=settings.postgres_database,
            user=settings.postgres_user,
            password=settings.postgres_password,
            port=int(settings.postgres_port),  # Ensure port is int
        )
        logger.info(f"PostgreSQL connection established to {settings.postgres_host}:{settings.postgres_port}/{settings.postgres_database}")
        return conn
    except psycopg2.OperationalError as e:
        error_msg = f"PostgreSQL connection failed: {e}. Check host, port, database, user, and password."
        logger.error(error_msg)
        raise ConnectionError(error_msg) from e
    except Exception as e:
        logger.error(f"DB connection error: {e}")
        raise

python3 market_feed_consumer.py
python3 finance_data_consumer.py
python3 client_data_consumer.py