import streamlit as st

from components import (
    render_check,
    render_go_further,
    render_header,
    render_key_concepts,
    render_learn,
    render_prompt,
    render_review,
    render_takeaways,
    render_tools,
)

render_header(1, "Discover the data", "0:20–0:35 (15 min)", "Know what's in the tables, and what isn't, before you trust a number.")

render_tools(
    [
        {"name": "CoCo side panel", "icon": "smart_toy", "description": "The AI assistant beside your SQL file. It reads table metadata, runs read-only queries you approve, and explains what it found."},
        {"name": "Workspaces SQL file", "icon": "edit_note", "description": "Your private scratch file in My Workspace. CoCo uses it as context and can write SQL into it."},
        {"name": "Snowflake Curated Data", "icon": "table_view", "description": "Free, ready-to-query public data from the Snowflake Marketplace. The lab uses a frozen snapshot of its daily stock prices."},
    ]
)

st.markdown(
    """
Before you analyze anything, find out four things: **what one row means** (the grain), **which measures exist**, **how fresh the data is**, and **what each measure doesn't tell you**. Market data has well-known traps on all four, and CoCo is good at surfacing them if you ask.
"""
)

render_prompt(
    "1.1",
    "Segments, freshness and caveats",
    """Using TMX_COCO_HOL.SOURCE.WATCHLIST, list the tickers by segment. Then tell me the latest available date in TMX_COCO_HOL.SOURCE.STOCK_PRICE_TIMESERIES and explain why it is not today. Explain the difference between post-market_close and post-market_close_adjusted, and what nasdaq_volume does and does not measure. Read-only.""",
)

render_review(
    [
        "Every statement CoCo wants to run is a `SELECT`, `SHOW` or `DESCRIBE`. Nothing creates, alters or drops.",
        "Table names are fully qualified (`TMX_COCO_HOL.SOURCE....`).",
        "Queries filter or group on `VARIABLE` rather than mixing all nine measures together.",
    ]
)

render_check(
    """
| Check | Expected |
| --- | --- |
| Exchange operators | NDAQ, ICE, CME, CBOE |
| Canadian interlisted | RY, TD, BMO, BNS, ENB, CNQ, SHOP |
| Benchmark ETFs | SPY, QQQ, EWC |
| Latest date | **2026-08-12**: the free data lags, and this lab uses a frozen snapshot |
| Adjusted close | Adjusted for dividends and splits. Example: RY on 2026-08-12 closes at **213.69**, adjusted **212.36** |
| Volume | CoCo should say `nasdaq_volume` is **Nasdaq-venue only**, not consolidated market volume |
"""
)

render_learn(
    "What this prompt does",
    """
CoCo usually answers in three moves. Each is a small read-only query you approve:

**1. Read the watchlist**
```sql
SELECT segment, ticker, company_name
FROM TMX_COCO_HOL.SOURCE.WATCHLIST
ORDER BY segment, ticker;
```

**2. Check freshness**
```sql
SELECT MIN(date), MAX(date), COUNT(DISTINCT date)
FROM TMX_COCO_HOL.SOURCE.STOCK_PRICE_TIMESERIES;
```

**3. Compare raw and adjusted on one day**
```sql
SELECT ticker, date, variable, value
FROM TMX_COCO_HOL.SOURCE.STOCK_PRICE_TIMESERIES
WHERE ticker = 'RY' AND date = '2026-08-12'
  AND variable IN ('post-market_close', 'post-market_close_adjusted');
```

The explanations of *adjusted* and *Nasdaq volume* come from CoCo's general knowledge combined with the column labels (`VARIABLE_NAME`). That's why the prompt asks it to **explain**, and why you should check the explanation against the numbers.
""",
)

render_go_further()

render_prompt(
    "1.2",
    "Completeness check",
    """For each ticker in TMX_COCO_HOL.SOURCE.WATCHLIST, count the trading days, distinct variables and rows in TMX_COCO_HOL.SOURCE.STOCK_PRICE_TIMESERIES. Flag any ticker that is missing days or variables compared with the others. Read-only.""",
    optional=True,
)

render_check(
    "Every ticker has **654 trading days, 9 variables and 5,886 rows**. Nothing is missing, so CoCo should report no gaps. A complete grid like this is what makes the later comparisons fair."
)

render_prompt(
    "1.3",
    "Where does each ticker list?",
    """Show each ticker's ASSET_CLASS, PRIMARY_EXCHANGE_CODE and PRIMARY_EXCHANGE_NAME from TMX_COCO_HOL.SOURCE.STOCK_PRICE_TIMESERIES, joined to its segment in TMX_COCO_HOL.SOURCE.WATCHLIST. Explain what this means for reading nasdaq_volume for NYSE-listed names. Read-only.""",
    optional=True,
)

render_check(
    """
| Listing | Tickers |
| --- | --- |
| New York Stock Exchange (`NYS`) | BMO, BNS, CNQ, ENB, ICE, RY, SHOP, TD |
| Nasdaq (`NAS`) | CME, NDAQ, QQQ |
| NYSE Arca (`PSE`) | EWC, SPY |
| Cboe BZX (`BAT`) | CBOE |

Asset classes: `Equity` for the 11 stocks; `ETF-Index Fund Shares` for EWC; `ETF-Portfolio Depositary Receipt` for SPY and QQQ.

The insight to look for: for **NYSE-listed** names, Nasdaq-venue volume is only a slice of their trading. Compare volume **over time for one ticker**, not **across tickers**.
"""
)

render_key_concepts(
    [
        ("Long (tall) format", "Each row holds one measure for one ticker on one day: `TICKER`, `DATE`, `VARIABLE`, `VALUE`. It's flexible, but you must filter or pivot on `VARIABLE` before aggregating."),
        ("Adjusted vs raw prices", "Raw prices are what traded. Adjusted prices are rescaled for dividends and splits so a return over time reflects what a holder earned. Use adjusted prices for returns."),
        ("Nasdaq-venue volume", "Shares traded on Nasdaq's venues only. US stocks trade on many venues, so this isn't the stock's total (consolidated) volume."),
        ("Interlisted", "A company listed on more than one exchange, such as RY on both TSX and NYSE. This lab only has the US listing, in USD."),
    ]
)

render_takeaways(
    [
        "Grounded CoCo in real tables using fully qualified names.",
        "Confirmed freshness, grain and the meaning of each measure.",
        "Kept CoCo read-only by saying so in the prompt and checking each SQL approval.",
    ]
)
