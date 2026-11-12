import streamlit as st

from components import (
    ctx,
    render_check,
    render_go_further,
    render_header,
    render_key_concepts,
    render_learn,
    render_prompt,
    render_review,
    render_takeaways,
    render_tools,
    require_context,
)

c = ctx()
P = c["prices"]

render_header(2, "Discover the data", "0:30–0:40 (10 min)", "Know what's in your table, and what isn't, before you trust a number.")
require_context()

render_tools(
    [
        {"name": "CoCo side panel", "icon": "smart_toy", "description": "The AI assistant beside your SQL file. It reads table metadata, runs read-only queries you approve, and explains what it found."},
        {"name": "Your Iceberg table", "icon": "ac_unit", "description": f"`{c['table']}`: 2026 prices for the S&P 500, copied from Snowflake Curated Data in exercise 1."},
        {"name": "Workspaces SQL file", "icon": "edit_note", "description": "Your private scratch file in My Workspace. CoCo uses it as context and can write SQL into it."},
    ]
)

st.markdown(
    """
Before you analyze anything, find out four things: **what one row means** (the grain), **which measures exist**, **how fresh the data is**, and **what each measure doesn't tell you**. Market data has well-known traps on all four, and CoCo is good at surfacing them if you ask.
"""
)

render_prompt(
    "2.1",
    "Grain, freshness and caveats",
    f"""Profile my Iceberg table {P}: its grain, the number of tickers, the first and latest DATE and the number of trading days. Explain why the latest date is not today. Using NDAQ on 2026-06-30 as an example, explain the difference between post-market_close and post-market_close_adjusted, and explain what nasdaq_volume does and does not measure. Read-only.""",
)

render_review(
    [
        "Every statement CoCo wants to run is a `SELECT`, `SHOW` or `DESCRIBE`. Nothing creates, alters or drops.",
        f"Queries read **your** table, `{P}`, not the Marketplace view.",
        "Queries filter or group on `VARIABLE` rather than mixing all nine measures together.",
    ]
)

render_check(
    """
| Check | Expected |
| --- | --- |
| Grain | One row per **ticker × date × variable** (long format) |
| Tickers | **503** |
| First date | **2026-01-02** |
| Latest date | About **three months before today**. The free tier lags, and your copy stops at the date you ran exercise 1. (2026-08-13 when this guide was checked.) |
| Adjusted close | Adjusted for dividends and splits. NDAQ on 2026-06-30 closes at **78.70**, adjusted **78.43** |
| Volume | CoCo should say `nasdaq_volume` is **Nasdaq-venue only**, not consolidated market volume |
"""
)

render_learn(
    "What this prompt does",
    f"""
CoCo usually answers in three moves. Each is a small read-only query you approve:

**1. Shape and freshness**
```sql
SELECT COUNT(DISTINCT ticker) AS tickers, MIN(date), MAX(date), COUNT(DISTINCT date) AS trading_days
FROM {P};
```

**2. The nine measures**
```sql
SELECT DISTINCT variable, variable_name FROM {P} ORDER BY variable;
```

**3. Raw vs adjusted on one day**
```sql
SELECT ticker, date, variable, value
FROM {P}
WHERE ticker = 'NDAQ' AND date = '2026-06-30'
  AND variable IN ('post-market_close', 'post-market_close_adjusted');
```

The explanations of *adjusted* and *Nasdaq volume* come from CoCo's general knowledge combined with the column labels (`VARIABLE_NAME`). That's why the prompt asks it to **explain**, and why you should check the explanation against the numbers.
""",
)

render_go_further()

render_prompt(
    "2.2",
    "Completeness check",
    f"""In {P}, count the trading days and distinct variables per ticker from 2026-01-02 to 2026-06-30. List every ticker that has fewer trading days than the maximum, with its first and last date in that window, and suggest why each one is short. Read-only.""",
    optional=True,
)

render_check(
    """
The window has **123 trading days**. 500 tickers have all 123 days and all 9 variables. Three don't:

| Ticker | Days | First date | Why |
| --- | --- | --- | --- |
| ECHO | 5 | 2026-06-24 | EchoStar, which traded as **SATS** until 2026-06-23 |
| BNY | 52 | 2026-01-02 | A **reused ticker**: a different security used `BNY` (at about $10, trading only some days) before Bank of New York Mellon moved to it from **BK** on 2026-05-21. The close jumps from about $10 to $139 that day |
| MRSH | 115 | 2026-01-14 | Marsh McLennan, which traded as **MMC** until 2026-01-13 |

The price data is keyed by **ticker, not company**. CoCo can spot the gaps, but the reason (a ticker change) comes from outside the data, so expect it as a suggestion. You'll exclude these three when ranking returns in exercise 4.
"""
)

render_prompt(
    "2.3",
    "Where do the S&P 500 stocks list?",
    f"""From {P}, count distinct tickers by PRIMARY_EXCHANGE_NAME and by ASSET_CLASS. Then show the listing exchange for NDAQ, ICE, CME and CBOE. Explain what this means for comparing nasdaq_volume between an NYSE-listed and a Nasdaq-listed stock. Read-only.""",
    optional=True,
)

render_check(
    """
| Primary exchange | Tickers |
| --- | --- |
| New York Stock Exchange | 346 |
| Nasdaq | 156 |
| BATS Z-Exchange (Cboe BZX) | 1, which is CBOE itself |

Asset classes: **Equity 473**, **REIT 26**, and four one-offs: BNY `Closed-End Funds` (left over from the ticker's previous owner), IT `Common Shares`, IVZ `Tracking Stock`, OTIS `Global Depositary Shares`. Labels in source metadata aren't always right.

The exchange operators: **NDAQ** and **CME** list on Nasdaq, **ICE** on NYSE, **CBOE** on Cboe BZX.

The insight to look for: for **NYSE-listed** names, Nasdaq-venue volume is only a slice of their trading. Compare volume **over time for one ticker**, not **across tickers**.
"""
)

render_key_concepts(
    [
        ("Long (tall) format", "Each row holds one measure for one ticker on one day: `TICKER`, `DATE`, `VARIABLE`, `VALUE`. It's flexible, but you must filter or pivot on `VARIABLE` before aggregating."),
        ("Adjusted vs raw prices", "Raw prices are what traded. Adjusted prices are rescaled for dividends and splits so a return over time reflects what a holder earned. Use adjusted prices for returns."),
        ("Nasdaq-venue volume", "Shares traded on Nasdaq's venues only. US stocks trade on many venues, so this isn't the stock's total (consolidated) volume."),
        ("Ticker vs company", "A ticker is a symbol, and companies change them. A gap at the start of a ticker's history, or a sudden price jump, often means a rename or a reused symbol."),
    ]
)

render_takeaways(
    [
        "Grounded CoCo in your own table using its fully qualified name.",
        "Confirmed freshness, grain and the meaning of each measure.",
        "Found the tickers that would distort a ranking, before ranking anything.",
    ]
)
