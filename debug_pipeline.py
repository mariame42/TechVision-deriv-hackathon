#!/usr/bin/env python3
"""
Debug script to check PostgreSQL pipeline connectivity and data.

Run this to diagnose why insights are returning 0:
1. Check database connection
2. Check table data exists
3. Test each insight calculation
4. Show what data is available
"""

import sys
import os

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✓ Loaded .env file")
except ImportError:
    print("⚠️  python-dotenv not installed, trying to read .env manually...")
    # Fallback: manually read .env file
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and full-line comments
                if not line or line.startswith('#'):
                    continue
                # Handle inline comments: split by # and take first part
                if '#' in line:
                    line = line.split('#')[0].strip()
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    # Remove quotes if present
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    os.environ[key] = value
        print("✓ Loaded .env file manually")

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.db import get_connection
from src.preprocessing import DataPreprocessor
from src.insights import InsightsEngine


def check_database_connection():
    """Test PostgreSQL connection."""
    print("=" * 70)
    print("1. DATABASE CONNECTION CHECK")
    print("=" * 70)
    
    # First, check if env vars are loaded
    print("\n   Checking environment variables...")
    env_vars = {
        "POSTGRES_HOST": os.getenv("POSTGRES_HOST"),
        "POSTGRES_DATABASE": os.getenv("POSTGRES_DATABASE"),
        "POSTGRES_USER": os.getenv("POSTGRES_USER"),
        "POSTGRES_PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "POSTGRES_PORT": os.getenv("POSTGRES_PORT"),
    }
    
    for key, value in env_vars.items():
        if value:
            # Mask password
            display_value = "***" if "PASSWORD" in key else value
            print(f"   ✓ {key}: {display_value}")
        else:
            print(f"   ✗ {key}: NOT SET")
    
    if not env_vars["POSTGRES_PASSWORD"]:
        print("\n   ⚠️  POSTGRES_PASSWORD is not set!")
        print("   Make sure your .env file has: POSTGRES_PASSWORD=your_password")
        print("   And that the .env file is in the project root directory.")
        return False
    
    try:
        conn = get_connection()
        print("\n   ✅ PostgreSQL connection successful!")
        
        # Test query
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"   PostgreSQL version: {version.split(',')[0]}")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"\n   ❌ Database connection failed: {e}")
        print("\n   Troubleshooting:")
        print("   1. Check .env file exists in project root")
        print("   2. Check .env has all required variables")
        print("   3. Check PostgreSQL is running")
        print("   4. Check host/port are correct")
        return False


def check_table_data():
    """Check if tables exist and have data."""
    print("\n" + "=" * 70)
    print("2. TABLE DATA CHECK")
    print("=" * 70)
    
    try:
        conn = get_connection()
        preprocessor = DataPreprocessor(conn)
        
        tables = ["daily_revenue", "client_activity", "market_prices"]
        
        for table_name in tables:
            print(f"\n📊 Table: {table_name}")
            df = preprocessor.fetch_table(table_name)
            
            if df.empty:
                print(f"   ⚠️  Table is EMPTY - no data found!")
            else:
                print(f"   ✅ Found {len(df)} rows")
                print(f"   Columns: {list(df.columns)}")
                
                # Show first few rows
                if len(df) > 0:
                    print(f"   First row sample:")
                    for col in df.columns[:5]:  # Show first 5 columns
                        val = df[col].iloc[0]
                        print(f"     {col}: {val}")
                
                # Show last row (most recent)
                if len(df) > 1:
                    print(f"   Last row sample:")
                    for col in df.columns[:5]:
                        val = df[col].iloc[-1]
                        print(f"     {col}: {val}")
        
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error checking tables: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_insight_calculations():
    """Test each insight calculation."""
    print("\n" + "=" * 70)
    print("3. INSIGHT CALCULATIONS TEST")
    print("=" * 70)
    
    try:
        conn = get_connection()
        preprocessor = DataPreprocessor(conn)
        engine = InsightsEngine(preprocessor)
        
        # Map of insight_id to method name
        insights_to_test = {
            1: ("trading_revenue_change", "Trading Revenue Change"),
            3: ("revenue_sensitivity_to_volatility", "Revenue Sensitivity to Volatility"),
            4: ("active_trader_change", "Active Trader Change"),
            7: ("volatility_regime_shift", "Volatility Regime Shift"),
            8: ("volume_contraction", "Volume Contraction"),
            9: ("asset_rotation_detection", "Asset Rotation Detection"),
            17: ("revenue_drop_root_cause", "Revenue Drop Root Cause"),
        }
        
        for insight_id, (method_name, display_name) in insights_to_test.items():
            print(f"\n🔍 Insight {insight_id}: {display_name}")
            try:
                method = getattr(engine, method_name)
                result = method()
                
                if result is None:
                    print(f"   ⚠️  Result: None")
                elif isinstance(result, dict):
                    if not result:
                        print(f"   ⚠️  Result: Empty dict {{}}")
                    else:
                        print(f"   ✅ Result: {result}")
                        for key, val in result.items():
                            print(f"      {key}: {val}")
                elif isinstance(result, (int, float)):
                    if result == 0:
                        print(f"   ⚠️  Result: 0 (might be correct or might indicate missing data)")
                    else:
                        print(f"   ✅ Result: {result}")
                else:
                    print(f"   ✅ Result: {result} (type: {type(result).__name__})")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
                import traceback
                traceback.print_exc()
        
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error testing insights: {e}")
        import traceback
        traceback.print_exc()
        return False


def check_data_requirements():
    """Check what data each insight needs."""
    print("\n" + "=" * 70)
    print("4. DATA REQUIREMENTS CHECK")
    print("=" * 70)
    
    try:
        conn = get_connection()
        preprocessor = DataPreprocessor(conn)
        
        # Check what data we have
        revenue_df = preprocessor.fetch_table("daily_revenue")
        activity_df = preprocessor.fetch_table("client_activity")
        prices_df = preprocessor.fetch_table("market_prices")
        
        print("\n📋 Required data for each insight:")
        print("\n   Insight 1 (Trading Revenue Change):")
        print("      Needs: daily_revenue table with at least 2 rows")
        print(f"      Has: {len(revenue_df)} rows")
        if len(revenue_df) >= 2:
            print(f"      ✅ Has 'total_revenue' column: {'total_revenue' in revenue_df.columns}")
            if 'total_revenue' in revenue_df.columns:
                print(f"      Latest values: {revenue_df['total_revenue'].iloc[-2:].tolist()}")
        else:
            print("      ⚠️  Need at least 2 rows for comparison")
        
        print("\n   Insight 3 (Revenue Sensitivity to Volatility):")
        print("      Needs: daily_revenue + market_prices with overlapping dates")
        print(f"      Has: {len(revenue_df)} revenue rows, {len(prices_df)} price rows")
        
        print("\n   Insight 4 (Active Trader Change):")
        print("      Needs: client_activity table with at least 2 rows")
        print(f"      Has: {len(activity_df)} rows")
        if len(activity_df) >= 2:
            print(f"      ✅ Has 'active' column: {'active' in activity_df.columns}")
            if 'active' in activity_df.columns:
                print(f"      Latest values: {activity_df['active'].iloc[-2:].tolist()}")
        
        print("\n   Insight 7 (Volatility Regime Shift):")
        print("      Needs: market_prices with at least 2 rows")
        print(f"      Has: {len(prices_df)} rows")
        if len(prices_df) >= 2:
            print(f"      ✅ Has 'price' and 'asset' columns: {'price' in prices_df.columns and 'asset' in prices_df.columns}")
        
        print("\n   Insight 8 (Volume Contraction):")
        print("      Needs: market_prices with 'volume' column")
        print(f"      Has: {len(prices_df)} rows")
        if len(prices_df) > 0:
            print(f"      ✅ Has 'volume' column: {'volume' in prices_df.columns}")
        
        print("\n   Insight 9 (Asset Rotation Detection):")
        print("      Needs: market_prices with 'asset' and 'volume' columns")
        print(f"      Has: {len(prices_df)} rows")
        if len(prices_df) > 0:
            print(f"      Assets: {prices_df['asset'].unique().tolist() if 'asset' in prices_df.columns else 'N/A'}")
        
        print("\n   Insight 17 (Revenue Drop Root Cause):")
        print("      Needs: All three tables with at least 2 rows each")
        print(f"      Has: {len(revenue_df)} revenue, {len(activity_df)} activity, {len(prices_df)} price rows")
        
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error checking requirements: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all diagnostic checks."""
    print("\n" + "=" * 70)
    print("POSTGRESQL PIPELINE DIAGNOSTIC TOOL")
    print("=" * 70)
    print("\nThis script will check:")
    print("  1. Database connection")
    print("  2. Table data availability")
    print("  3. Insight calculations")
    print("  4. Data requirements")
    print("\n" + "=" * 70 + "\n")
    
    # Run checks
    conn_ok = check_database_connection()
    
    if not conn_ok:
        print("\n❌ Cannot proceed - database connection failed!")
        print("   Fix connection issues first, then run again.")
        return
    
    check_table_data()
    check_data_requirements()
    test_insight_calculations()
    
    print("\n" + "=" * 70)
    print("DIAGNOSTIC COMPLETE")
    print("=" * 70)
    print("\nIf all insights return 0, check:")
    print("  1. Tables have data (at least 2 rows for comparisons)")
    print("  2. Column names match expected names")
    print("  3. Data types are correct (numbers, not strings)")
    print("  4. Date/created_at columns are properly formatted")
    print("\n")


if __name__ == "__main__":
    main()

