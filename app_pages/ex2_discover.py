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
        {"name": "Your Iceberg table", "icon": "ac_unit", "description": f"`{c['table']}`: every US listing's 2026 prices, copied from Snowflake Curated Data in exercise 1."},
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
| Tickers | About **13,900** (13,924 when this guide was checked): stocks, ETFs and funds |
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
    f"""In {P}, from 2026-01-02 to 2026-06-30, count how many tickers have every trading day and all 9 variables, and how many don't. Split the incomplete ones into: started after 2026-01-02, ended before 2026-06-30, both, or gaps in between. Then show the trading-day count for NDAQ, ICE, CME, CBOE, SPY, QQQ and EWC, and for BK, BNY, MMC, MRSH, SATS and ECHO, and suggest why the last six are short. Read-only.""",
    optional=True,
)

render_check(
    """
The window has **123 trading days** and **13,534 tickers**. **7,534** have all 123 days and all 9 variables; **6,000** don't:

| Why short | Tickers |
| --- | --- |
| Started after 2026-01-02 (new listings, renames) | 1,629 |
| Ended before 2026-06-30 (delistings, renames) | 1,091 |
| Both | 1,046 |
| Gaps in between (thinly traded) | 2,234 |

NDAQ, ICE, CME, CBOE, SPY, QQQ and EWC each have all **123** days. The six named tickers are three **ticker changes**:

| Old ticker | Days | New ticker | Days | What happened |
| --- | --- | --- | --- | --- |
| MMC | 8 | MRSH | 115 | Marsh McLennan moved to MRSH on 2026-01-14 |
| BK | 96 | BNY | 52 | Bank of New York Mellon moved to BNY on 2026-05-21. `BNY` was a **reused ticker**: a different, $10 security used it before, so its close jumps from about $10 to $139 that day |
| SATS | 118 | ECHO | 5 | EchoStar moved to ECHO on 2026-06-24 |

The price data is keyed by **ticker, not company**. CoCo can spot the gaps, but the reason (a ticker change) comes from outside the data, so expect it as a suggestion. Any ranking across many tickers must exclude incomplete ones first.
"""
)

render_prompt(
    "2.3",
    "Where do the tickers list?",
    f"""From {P}, for 2026-01-02 to 2026-06-30, count distinct tickers by PRIMARY_EXCHANGE_NAME and by ASSET_CLASS. Then show the listing exchange and asset class for NDAQ, ICE, CME, CBOE, SPY, QQQ, EWC, RY, TD, BMO, BNS, ENB, CNQ and SHOP. Explain what this means for comparing nasdaq_volume between an NYSE-listed and a Nasdaq-listed stock. Read-only.""",
    optional=True,
)

render_check(
    """
| Primary exchange | Tickers |
| --- | --- |
| Nasdaq | 5,875 |
| New York Stock Exchange | 3,096 |
| NYSE Arca | 2,770 |
| BATS Z-Exchange (Cboe BZX) | 1,448 |
| NYSE American (`NYSE MKT LLC`) | 335 |
| No value | 10 |

Largest asset classes: **Equity 7,194**, **ETF-Index Fund Shares 5,473**, Closed-End Funds 339, Global Shares 204, REIT 134.

| Listing | Tickers |
| --- | --- |
| New York Stock Exchange (`NYS`) | ICE, RY, TD, BMO, BNS, ENB, CNQ, SHOP |
| Nasdaq (`NAS`) | NDAQ, CME, QQQ |
| NYSE Arca (`PSE`) | SPY, EWC |
| Cboe BZX (`BAT`) | CBOE |

The 11 stocks are `Equity`; EWC is `ETF-Index Fund Shares`; SPY and QQQ are `ETF-Portfolio Depositary Receipt`. RY to SHOP are **Canadian interlisted** companies: this is their US listing, in USD.

The insight to look for: for **NYSE-listed** names, Nasdaq-venue volume is only a slice of their trading. Compare volume **over time for one ticker**, not **across tickers**.
"""
)

render_key_concepts(
    [
        ("Long (tall) format", "Each row holds one measure for one ticker on one day: `TICKER`, `DATE`, `VARIABLE`, `VALUE`. It's flexible, but you must filter or pivot on `VARIABLE` before aggregating."),
        ("Adjusted vs raw prices", "Raw prices are what traded. Adjusted prices are rescaled for dividends and splits so a return over time reflects what a holder earned. Use adjusted prices for returns."),
        ("Nasdaq-venue volume", "Shares traded on Nasdaq's venues only. US stocks trade on many venues, so this isn't the stock's total (consolidated) volume."),
        ("Interlisted", "A company listed on more than one exchange, such as RY on both TSX and NYSE. Your table has only the US listing, in USD."),
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
