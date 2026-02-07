"""
Data preprocessing layer.

Handles:
- Data fetching from PostgreSQL
- Data cleaning
- Basic transformations
"""

import pandas as pd
import logging
from typing import Optional
import psycopg2

logger = logging.getLogger(__name__)


class DataPreprocessor:
    """
    Fetch and clean data for insights.
    
    This layer is responsible for:
    - Fetching full tables from PostgreSQL
    - Handling missing values
    - Basic data transformations
    """
    
    def __init__(self, conn: psycopg2.extensions.connection):
        """
        Initialize the data preprocessor.
        
        Args:
            conn: PostgreSQL connection object
        """
        self.conn = conn
    
    def fetch_table(self, table_name: str) -> pd.DataFrame:
        """
        Fetch full table from PostgreSQL.
        
        Args:
            table_name: Name of the table to fetch
            
        Returns:
            pd.DataFrame: Table data with missing values filled (0)
        """
        try:
            query = f'SELECT * FROM "{table_name}"'
            df = pd.read_sql(query, self.conn)
            df = df.fillna(0)
            logger.info(f"Fetched {len(df)} rows from {table_name}")
            return df
        except Exception as e:
            logger.error(f"Error fetching {table_name}: {e}")
            return pd.DataFrame()
    
    @staticmethod
    def safe_pct_change(current: float, previous: float) -> float:
        """
        Calculate safe percentage change, avoiding division by zero.
        
        Args:
            current: Current value
            previous: Previous value
            
        Returns:
            float: Percentage change, or 0 if previous is 0
        """
        try:
            if previous == 0:
                return 0
            return ((current - previous) / previous) * 100
        except Exception as e:
            logger.error(f"Error calculating pct change: {e}")
            return 0

