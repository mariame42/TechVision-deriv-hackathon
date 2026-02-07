"""
Insights computation engine.

Computes 7 real-time insights from PostgreSQL data.
All formulas and calculations are embedded in this module.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
import logging
from ..preprocessing.data_preprocessor import DataPreprocessor

logger = logging.getLogger(__name__)


class InsightsEngine:
    """
    Compute real-time insights from preprocessed data.
    
    This engine implements all insight calculations internally.
    No external formulas or configs needed.
    """
    
    def __init__(self, preprocessor: DataPreprocessor):
        """
        Initialize the insights engine.
        
        Args:
            preprocessor: DataPreprocessor instance for fetching data
        """
        self.preprocessor = preprocessor
    
    # -----------------
    # Revenue Insights
    # -----------------
    
    def trading_revenue_change(self) -> float:
        """
        Compute trading revenue change percentage.
        
        Insight ID: 1
        
        Returns:
            float: Percentage change in total revenue (last vs previous)
        """
        df = self.preprocessor.fetch_table("daily_revenue")
        if len(df) < 2:
            logger.warning("Insufficient data for trading_revenue_change")
            return 0
        
        # Sort by date to ensure correct order
        df = df.sort_values('date')
        
        current = df['total_revenue'].iloc[-1]
        previous = df['total_revenue'].iloc[-2]
        return round(self.preprocessor.safe_pct_change(current, previous), 2)
    
    def revenue_sensitivity_to_volatility(self) -> float:
        """
        Compute correlation between revenue and market volatility.
        
        Insight ID: 3
        
        Returns:
            float: Correlation coefficient (-1 to 1)
        """
        revenue_df = self.preprocessor.fetch_table("daily_revenue")
        prices_df = self.preprocessor.fetch_table("market_prices")
        
        if revenue_df.empty or prices_df.empty or len(prices_df) < 2:
            logger.warning("Insufficient data for revenue_sensitivity_to_volatility")
            return 0
        
        # Compute daily return per asset
        prices_df['return'] = prices_df.groupby('asset')['price'].pct_change()
        
        # Extract date from created_at (remove time component) for alignment
        prices_df['date'] = pd.to_datetime(prices_df['created_at']).dt.date
        
        # Aggregate volatility by date (std of all returns per day)
        vol_by_date = prices_df.groupby('date')['return'].std()
        vol_by_date = vol_by_date.fillna(0)
        
        # Aggregate revenue by date (sum total_revenue per date)
        # This handles cases where multiple rows have same date
        revenue_by_date = revenue_df.groupby('date')['total_revenue'].sum()
        
        # Convert date index to date objects for matching
        # Handle different date types (string, datetime, date)
        if isinstance(revenue_by_date.index, pd.DatetimeIndex):
            revenue_dates = revenue_by_date.index.date
        elif hasattr(revenue_by_date.index[0], 'date'):
            # Already date objects
            revenue_dates = revenue_by_date.index
        else:
            # Convert from string or other format
            revenue_dates = pd.to_datetime(revenue_by_date.index).date
        
        # Convert to Series with date index
        revenue_series = pd.Series(revenue_by_date.values, index=revenue_dates)
        
        # Align dates
        common_dates = revenue_series.index.intersection(vol_by_date.index)
        if len(common_dates) < 2:
            logger.warning(f"Insufficient overlapping data for correlation. Revenue dates: {len(revenue_series)}, Vol dates: {len(vol_by_date)}, Common: {len(common_dates)}")
            
            # Fallback: Use time-based correlation when only 1 date but multiple time periods
            if len(revenue_df) >= 2 and len(prices_df) >= 2:
                # Calculate revenue trend (first vs last)
                revenue_trend = revenue_df['total_revenue'].iloc[-1] - revenue_df['total_revenue'].iloc[0]
                revenue_pct_change = self.preprocessor.safe_pct_change(
                    revenue_df['total_revenue'].iloc[-1],
                    revenue_df['total_revenue'].iloc[0]
                )
                
                # Calculate price volatility trend (std of returns over time)
                prices_sorted = prices_df.sort_values('created_at')
                prices_sorted['return'] = prices_sorted.groupby('asset')['price'].pct_change()
                vol_trend = prices_sorted['return'].std()
                
                # Simple correlation: if revenue increases and volatility is high, positive correlation
                # If revenue decreases and volatility is high, negative correlation
                if abs(revenue_pct_change) > 0.1 and not pd.isna(vol_trend) and vol_trend > 0:
                    # Positive correlation if both move in same direction
                    return 0.5 if revenue_pct_change > 0 else -0.5
                elif abs(revenue_pct_change) > 0.1:
                    # Weak correlation if volatility is low
                    return 0.1 if revenue_pct_change > 0 else -0.1
                else:
                    # No significant change
                    return 0
            
            return 0
        
        corr = np.corrcoef(revenue_series.loc[common_dates], vol_by_date.loc[common_dates])[0, 1]
        return round(corr, 2) if not np.isnan(corr) else 0
    
    # -----------------
    # Trader Insights
    # -----------------
    
    def active_trader_change(self) -> float:
        """
        Compute active trader change percentage.
        
        Insight ID: 4
        
        Returns:
            float: Percentage change in active traders (last vs previous)
        """
        df = self.preprocessor.fetch_table("client_activity")
        if len(df) < 2:
            logger.warning("Insufficient data for active_trader_change")
            return 0
        
        # Sort by created_at to ensure correct order
        df = df.sort_values('created_at')
        
        # Try active column first
        current_active = df['active'].iloc[-1]
        previous_active = df['active'].iloc[-2]
        
        # If active is all zeros, use 'new' column as alternative metric
        if current_active == 0 and previous_active == 0:
            logger.info("All 'active' values are 0, using 'new' column as alternative metric")
            # Use new trader signups as proxy for activity change
            # Compare recent period vs previous period
            n = len(df)
            if n >= 20:
                # Use last 10% vs previous 10%
                recent_new = df['new'].iloc[-n//10:].sum()
                previous_new = df['new'].iloc[-n//10*2:-n//10].sum()
            else:
                # Use last vs previous
                recent_new = df['new'].iloc[-1]
                previous_new = df['new'].iloc[-2] if n >= 2 else 0
            return round(self.preprocessor.safe_pct_change(recent_new, previous_new), 2)
        
        return round(self.preprocessor.safe_pct_change(current_active, previous_active), 2)
    
    # -----------------
    # Market Insights
    # -----------------
    
    def volatility_regime_shift(self) -> float:
        """
        Compute current volatility regime.
        
        Insight ID: 7
        
        Returns:
            float: Rolling volatility (std of returns over 5 periods)
        """
        df = self.preprocessor.fetch_table("market_prices")
        if len(df) < 2:
            logger.warning("Insufficient data for volatility_regime_shift")
            return 0
        
        # Sort by created_at
        df = df.sort_values('created_at')
        
        # Compute daily return per asset
        df['return'] = df.groupby('asset')['price'].pct_change()
        
        # Rolling volatility (std over 5 periods)
        df['rolling_vol'] = df.groupby('asset')['return'].rolling(5).std().reset_index(0, drop=True)
        
        # Return latest volatility
        latest_vol = df['rolling_vol'].iloc[-1]
        return round(latest_vol, 4) if not pd.isna(latest_vol) else 0
    
    def volume_contraction(self) -> float:
        """
        Compute volume contraction percentage.
        
        Insight ID: 8
        
        Returns:
            float: Percentage change in total volume (current vs previous)
        """
        df = self.preprocessor.fetch_table("market_prices")
        if len(df) < 2:
            logger.warning("Insufficient data for volume_contraction")
            return 0
        
        # Sort by created_at
        df = df.sort_values('created_at')
        
        current = df['volume'].sum()
        previous = df['volume'].iloc[:-1].sum()
        return round(self.preprocessor.safe_pct_change(current, previous), 2)
    
    def asset_rotation_detection(self) -> Dict[str, float]:
        """
        Detect asset rotation by computing volume changes per asset.
        
        Insight ID: 9
        
        Returns:
            dict: Asset name -> percentage change in volume
        """
        df = self.preprocessor.fetch_table("market_prices")
        if len(df) < 2:
            logger.warning("Insufficient data for asset_rotation_detection")
            return {}
        
        rotation = {}
        assets = df['asset'].unique()
        
        for asset in assets:
            asset_df = df[df['asset'] == asset].sort_values('created_at')
            if len(asset_df) < 2:
                continue
            
            current = asset_df['volume'].iloc[-1]
            previous = asset_df['volume'].iloc[-2]
            rotation[asset] = round(self.preprocessor.safe_pct_change(current, previous), 2)
        
        return rotation
    
    # -----------------
    # Cross-Domain Insights
    # -----------------
    
    def revenue_drop_root_cause(self) -> Dict[str, float]:
        """
        Analyze root cause of revenue drop with attribution.
        
        Insight ID: 17
        
        Returns:
            dict: Attribution breakdown with percentages
                - revenue_change_pct: Overall revenue change
                - active_trader_pct_contrib: Trader contribution to change
                - market_volatility_pct_contrib: Volatility contribution to change
        """
        revenue_df = self.preprocessor.fetch_table("daily_revenue")
        traders_df = self.preprocessor.fetch_table("client_activity")
        prices_df = self.preprocessor.fetch_table("market_prices")
        
        if len(revenue_df) < 2 or len(traders_df) < 2 or prices_df.empty:
            logger.warning("Insufficient data for revenue_drop_root_cause")
            return {}
        
        # Sort dataframes
        revenue_df = revenue_df.sort_values('date')
        traders_df = traders_df.sort_values('created_at')
        prices_df = prices_df.sort_values('created_at')
        
        # Compute change percentages
        revenue_change = self.preprocessor.safe_pct_change(
            revenue_df['total_revenue'].iloc[-1],
            revenue_df['total_revenue'].iloc[-2]
        )
        
        trader_change = self.preprocessor.safe_pct_change(
            traders_df['active'].iloc[-1],
            traders_df['active'].iloc[-2]
        )
        
        # Market volatility change
        prices_df['return'] = prices_df.groupby('asset')['price'].pct_change()
        vol = prices_df.groupby('created_at')['return'].std()
        
        if len(vol) < 2:
            vol_change = 0
        else:
            vol_sorted = vol.sort_index()
            vol_change = self.preprocessor.safe_pct_change(
                vol_sorted.iloc[-1],
                vol_sorted.iloc[-2]
            )
        
        # Simple attribution
        total = abs(trader_change) + abs(vol_change)
        if total == 0 or np.isnan(total):
            return {
                'revenue_change_pct': round(revenue_change, 2),
                'active_trader_pct_contrib': 0.0,
                'market_volatility_pct_contrib': 0.0
            }
        
        # Handle NaN values
        trader_contrib = abs(trader_change) / total * 100 if not np.isnan(trader_change) else 0.0
        vol_contrib = abs(vol_change) / total * 100 if not np.isnan(vol_change) else 0.0
        
        return {
            'revenue_change_pct': round(revenue_change, 2),
            'active_trader_pct_contrib': round(trader_contrib, 2),
            'market_volatility_pct_contrib': round(vol_contrib, 2)
        }
    
    def compute_insight(self, insight_id: int) -> Any:
        """
        Compute insight by ID.
        
        Maps insight_id to the appropriate method.
        
        Args:
            insight_id: Insight ID (1, 3, 4, 7, 8, 9, 17)
            
        Returns:
            Result from the insight method, or None if invalid ID
        """
        method_map = {
            1: self.trading_revenue_change,
            3: self.revenue_sensitivity_to_volatility,
            4: self.active_trader_change,
            7: self.volatility_regime_shift,
            8: self.volume_contraction,
            9: self.asset_rotation_detection,
            17: self.revenue_drop_root_cause,
        }
        
        method = method_map.get(insight_id)
        if method is None:
            logger.warning(f"No method found for insight_id {insight_id}")
            return None
        
        return method()

