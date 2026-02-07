"""
Insight ID mappings (1-18).

This module maps Insight IDs to their names.
Used by:
- Classifier node: to get insight names for classification and display
"""

from typing import Dict

# we have 18 insights, those 7 are the ones that
# we can implement for having the currunt data bases
# the first 6 will calclate numbers and resones
# the last one will be just reasoning and not calclating numbers

# 1.Trading Revenue Change
# 2.Revenue Sensitivity to Volatility
# 3.Active Trader Change
# 4.Volatility Regime Shift
# 5.Volume Contraction
# 6.Asset Rotation Detection
# 7.Revenue Drop Root Cause Chain

# Map of Insight ID to insight name
INSIGHT_MAP: Dict[int, Dict[str, str]] = {
    1: {
        "Trading revenue change": {}
    },
    2: {
        "Revenue per segment": {}
    },
    3: {
        "Revenue sensitivity to volatility": {}
    },
    4: {
        "Active trader change": {}
    },
    5: {
        "VIP migration": {}
    },
    6: {
        "Deposit / withdrawal anomaly": {}
    },
    7: {
        "Volatility regime shift": {}
    },
    8: {
        "Volume contraction": {}
    },
    9: {
        "Asset rotation detection": {}
    },
    10: {
        "Exposure concentration": {}
    },
    11: {
        "Leverage spike": {}
    },
    12: {
        "Margin call acceleration": {}
    },
    13: {
        "Latency impact": {}
    },
    14: {
        "Order rejection spike": {}
    },
    15: {
        "Fee change impact": {}
    },
    16: {
        "Market share shift": {}
    },
    17: {
        "Revenue drop root cause chain": {}
    },
    18: {
        "Risk surge root cause chain": {}
    },
}

# Revenue

# 1. Trading revenue change

# 2. Revenue per segment

# 3. Revenue sensitivity to volatility

# Traders

# 4. Active trader change

# 5. VIP migration

# 6. Deposit / withdrawal anomaly

# Market

# 7. Volatility regime shift

# 8. Volume contraction

# 9. Asset rotation detection

# Risk

# 10. Exposure concentration

# 11. Leverage spike

# 12. Margin call acceleration

# Platform

# 13. Latency impact

# 14. Order rejection spike

# Competitive

# 15. Fee change impact

# 16. Market share shift

# Cross-Domain

# 17. Revenue drop root cause chain

# 18. Risk surge root cause chain



# Here are 3 distinct user questions for each of the 18 insights. These are designed to train your Intent Classifier (Node C) to recognize different ways a user might ask for the same analysis.

# Revenue
# 1. Trading revenue change

# "How does today's trading revenue compare to the same time yesterday?"

# "Are we seeing a positive or negative trend in revenue this week?"

# "What is the day-over-day percentage change in our total trading fees?"

# 2. Revenue per segment

# "Break down our current revenue by VIP vs. Retail traders."

# "Which user segment is driving the most revenue growth right now?"

# "Is the API segment underperforming compared to manual traders?"

# 3. Revenue sensitivity to volatility

# "Did the recent spike in Bitcoin volatility increase our revenue?"

# "What is the correlation between VIX and our trading fees this month?"

# "Are we making more money from this volatility, or is volume staying flat?"

# Traders
# 4. Active trader change

# "Why is the number of active traders dropping today?"

# "Show me the week-over-week growth in daily active users."

# "Did we have more traders online during the Asia session or the US session?"

# 5. VIP migration

# "Have any key VIP clients stopped trading in the last 7 days?"

# "Are we seeing a churn risk in our high-net-worth segment?"

# "List the top VIPs who haven't placed an order this week."

# 6. Deposit / withdrawal anomaly

# "Flag any unusually large withdrawals from the last hour."

# "Are there any suspicious deposit patterns happening right now?"

# "Is net flow positive or negative for the day?"

# Market
# 7. Volatility regime shift

# "Have we officially entered a high-volatility regime?"

# "Is the current market calmness unusual compared to historical averages?"

# "Detect if there is a breakout in asset price volatility."

# 8. Volume contraction

# "Why is trading volume drying up across the board?"

# "Are we in a period of volume contraction compared to last month?"

# "Is the low volume specific to Crypto or is it happening in FX too?"

# 9. Asset rotation detection

# "Are traders rotating capital out of Bitcoin and into Altcoins?"

# "Where is the money flowing? Detect any sector rotation."

# "Is there a shift in volume from Major pairs to Exotics?"

# Risk
# 10. Exposure concentration

# "Do we have dangerous exposure levels in any single asset?"

# "What are our top 3 concentration risks right now?"

# "Are we over-exposed to Gold significantly more than usual?"

# 11. Leverage spike

# "Is the average trader leverage increasing dangerously?"

# "Show me the trend of open interest vs. margin used."

# "Are retail traders taking on higher leverage ratios today?"

# 12. Margin call acceleration

# "Are we seeing an acceleration in margin calls right now?"

# "Is the rate of liquidations abnormal for this price move?"

# "Alert me if margin calls exceed the hourly threshold."

# Platform
# 13. Latency impact

# "Did the system latency spike at 9:00 AM affect our volume?"

# "Quantify the estimated revenue loss due to platform lag today."

# "Is execution speed slowing down trading activity?"

# 14. Order rejection spike

# "Why are we seeing a sudden spike in order rejections?"

# "Is the high rejection rate due to technical errors or risk blocks?"

# "Show me the rejection rate for API orders specifically."

# Competitive
# 15. Fee change impact

# "Did lowering our maker fees result in higher volume?"

# "Analyze the impact of last week's fee schedule change on revenue."

# "Are we losing revenue because of the new fee structure?"

# 16. Market share shift

# "Is our volume growing faster or slower than the overall market?"

# "Did we gain market share during the volatility yesterday?"

# "Compare our volume trend against the major competitor index."

# Cross-Domain (Deep Reasoning)
# 17. Revenue drop root cause chain

# "Why did our revenue drop yesterday despite high volatility?"

# "Diagnose the main reason for the decline in trading fees today."

# "Is the revenue drop caused by technical issues or just low market interest?"

# 18. Risk surge root cause chain

# "What is the root cause of the sudden spike in our risk profile?"

# "Why are liquidations surging even though price is stable?"

# "Explain why our exposure concentration jumped in the last hour."
