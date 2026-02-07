# Math Engine - Insight-Based Formulas

## Overview

The Math Engine now uses **insight-specific formulas** defined in `src/config/insights.py`. Each insight can have custom formulas that calculate derived metrics based on the fetched data.

## How It Works

### Flow

1. **Classifier** → Determines `insight_id` (1-18) and `required_metrics`
2. **Hybrid Fetcher** → Fetches raw data for `required_metrics` → `fetched_data`
3. **Math Engine** → Uses `insight_id` to look up formulas → Executes formulas with `fetched_data` → `derived_data`
4. **Analyst** → Uses both `fetched_data` + `derived_data` to generate insights

### Formula Structure

Each insight in `INSIGHT_MAP` can have a `formulas` dictionary:

```python
{
    "Insight Name": {
        "required_metrics": ["internal_revenue", "internal_revenue_previous"],
        "formulas": {
            "revenue_change": lambda data: (
                (data.get("internal_revenue", 0) - data.get("internal_revenue_previous", 0)) 
                / data.get("internal_revenue_previous", 1) * 100 
                if data.get("internal_revenue_previous", 0) > 0 else 0
            ),
            "revenue_change_absolute": lambda data: (
                data.get("internal_revenue", 0) - data.get("internal_revenue_previous", 0)
            ),
        }
    }
}
```

## Example: Insight 1 (Trading Revenue Change)

### Configuration

```python
1: {
    "Trading revenue change": {
        "required_metrics": ["internal_revenue", "internal_revenue_previous"],
        "formulas": {
            "revenue_change": lambda data: (
                (data.get("internal_revenue", 0) - data.get("internal_revenue_previous", 0)) 
                / data.get("internal_revenue_previous", 1) * 100 
                if data.get("internal_revenue_previous", 0) > 0 else 0
            ),
            "revenue_change_absolute": lambda data: (
                data.get("internal_revenue", 0) - data.get("internal_revenue_previous", 0)
            ),
        }
    },
}
```

### Execution

1. **Fetcher** gets:
   ```python
   fetched_data = {
       "internal_revenue": 100000,
       "internal_revenue_previous": 95000
   }
   ```

2. **Math Engine** executes formulas:
   ```python
   derived_data = {
       "revenue_change": 5.26,  # (100000 - 95000) / 95000 * 100
       "revenue_change_absolute": 5000  # 100000 - 95000
   }
   ```

3. **Analyst** receives both:
   ```python
   data_context = {
       **fetched_data,  # Raw data
       **derived_data   # Calculated metrics
   }
   ```

## Example: Insight 17 (Revenue Drop Root Cause Chain)

### Configuration

```python
17: {
    "Revenue drop root cause chain": {
        "required_metrics": [
            "internal_revenue",
            "internal_revenue_previous",
            "internal_latency",
            "internal_volatility",
            "external_btc_price",
            "external_market_volatility",
        ],
        "formulas": {
            "revenue_drop_percentage": lambda data: (
                (data.get("internal_revenue", 0) - data.get("internal_revenue_previous", 0))
                / data.get("internal_revenue_previous", 1) * 100
                if data.get("internal_revenue_previous", 0) > 0 else 0
            ),
            "volatility_ratio": lambda data: (
                data.get("external_market_volatility", 0) / data.get("internal_volatility", 1)
                if data.get("internal_volatility", 0) > 0 else 0
            ),
            "latency_impact_score": lambda data: (
                data.get("internal_latency", 0) * 0.1
            ),
        }
    },
}
```

## Adding Formulas to New Insights

### Step 1: Add `formulas` to insight config

```python
5: {
    "VIP migration": {
        "required_metrics": ["internal_vip_migration", "internal_vip_count_previous"],
        "formulas": {
            "vip_migration_rate": lambda data: (
                data.get("internal_vip_migration", 0) / data.get("internal_vip_count_previous", 1) * 100
                if data.get("internal_vip_count_previous", 0) > 0 else 0
            ),
        }
    },
}
```

### Step 2: Ensure `required_metrics` match formula needs

The formulas use `data.get("metric_name")`, so make sure:
- All metrics used in formulas are in `required_metrics`
- Metric names match exactly (case-sensitive)

### Step 3: Test

The Math Engine will automatically:
- Look up formulas for the `insight_id`
- Execute each formula with `fetched_data`
- Store results in `derived_data`
- Log success/failure for each formula

## Fallback Behavior

If an insight doesn't have formulas defined:
- Math Engine uses default calculations (volatility ratio, revenue-BTC correlation)
- Logs a warning: `"No formulas defined for Insight X, using default calculations"`

## Formula Best Practices

1. **Use lambda functions** for simple calculations
2. **Handle missing data** with `.get()` and defaults
3. **Avoid division by zero** - always check denominators
4. **Return meaningful values** - numbers, strings, or None (not exceptions)
5. **Keep formulas simple** - complex logic should be in separate functions

## Example Formula Patterns

### Percentage Change
```python
"change_percentage": lambda data: (
    (data.get("current", 0) - data.get("previous", 0))
    / data.get("previous", 1) * 100
    if data.get("previous", 0) > 0 else 0
)
```

### Ratio
```python
"ratio": lambda data: (
    data.get("numerator", 0) / data.get("denominator", 1)
    if data.get("denominator", 0) > 0 else 0
)
```

### Classification
```python
"regime": lambda data: (
    "high" if data.get("value", 0) > threshold
    else "low" if data.get("value", 0) < threshold
    else "normal"
)
```

## Current Status

✅ **Insights with formulas:**
- Insight 1: Trading revenue change
- Insight 3: Revenue sensitivity to volatility
- Insight 4: Active trader change
- Insight 7: Volatility regime shift
- Insight 17: Revenue drop root cause chain

📝 **Insights without formulas (use defaults):**
- All other insights (2, 5, 6, 8-16, 18)

## Next Steps

1. Add formulas for remaining insights (2, 5, 6, 8-16, 18)
2. Test formulas with real data
3. Add validation for formula results
4. Consider adding formula dependencies/ordering if needed

