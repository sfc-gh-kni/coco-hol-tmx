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

render_header(4, "Compare trends", "0:55–1:05 (10 min)", "Compare first-half returns and find the biggest moves, with window functions.")
require_context()

st.info(
    "If it's already past 1:05, skip to **5. Build and deploy an app**. You can come back to this later.",
    icon=":material/timer:",
)

render_tools(
    [
        {"name": "Window functions", "icon": "functions", "description": "`LAG`, running `MAX` and `ROW_NUMBER` compare each row with its neighbours without a self-join."},
        {"name": "QUALIFY", "icon": "rule", "description": "Snowflake's filter on window-function results: the window-function equivalent of `HAVING`."},
        {"name": "MIN_BY / MAX_BY", "icon": "calculate", "description": "Return the value at the earliest or latest date in one pass: the first and last close of a period."},
    ]
)

st.markdown(
    """
The window is fixed at **2026-01-02 to 2026-06-30** (the first half), so your answers match the guide whenever you copied the data. You'll compare 14 tickers in three groups:

| Group | Tickers |
| --- | --- |
| Exchange operators | NDAQ, ICE, CME, CBOE |
| Benchmark ETFs | SPY (S&P 500), QQQ (Nasdaq-100), EWC (MSCI Canada) |
| Canadian interlisted (US listings) | RY, TD, BMO, BNS, ENB, CNQ, SHOP |
"""
)

render_prompt(
    "4.1",
    "First-half returns and largest daily moves",
    f"""Using post-market_close_adjusted in {P}, compute the return from 2026-01-02 to 2026-06-30 for these tickers, labelled by group: exchange operators NDAQ, ICE, CME, CBOE; benchmark ETFs SPY, QQQ, EWC; Canadian interlisted RY, TD, BMO, BNS, ENB, CNQ, SHOP. Show the first and last date and the number of trading days for each, and sort by return descending. Then, for the four exchange operators, find each one's largest single-day percent move in the same window using a window function, and explain how you handled the first trading day of 2026.""",
)

render_review(
    [
        "The query uses `post-market_close_adjusted`, not the raw close.",
        "Every ticker shows **123** trading days and dates **2026-01-02 to 2026-06-30**.",
        "The largest move is ranked by **absolute** change, so big drops count as well as big gains.",
        "Rows whose previous close is `NULL` are filtered out before ranking the moves.",
    ]
)

render_check(
    """
| Group | Return, 2026-01-02 to 2026-06-30 (adjusted close) |
| --- | --- |
| Canadian interlisted | BMO +34.89%, TD +30.34%, RY +22.91%, BNS +19.11%, CNQ +18.02%, ENB +16.02%, SHOP −27.44% |
| Benchmark ETF | QQQ +20.30%, SPY +9.90%, EWC +6.86% |
| Exchange operator | CBOE −2.30%, CME −15.67%, NDAQ −18.26%, ICE −22.82% |

All four exchange operators trailed every benchmark ETF. SHOP is the only name lower than ICE.

Largest single-day moves:

| Ticker | Move | Date |
| --- | --- | --- |
| NDAQ | −9.69% | 2026-02-03 |
| CBOE | −9.61% | 2026-06-16 |
| ICE | −7.49% | 2026-02-11 |
| CME | −5.80% | 2026-06-01 |

**If every move is dated 2026-01-02 with a blank value**, the `NULL` previous close wasn't filtered (see below).
"""
)

render_learn(
    "What this prompt does, and the first-day trap",
    f"""
**Returns: first and last value per ticker**
```sql
WITH tickers (ticker, grp) AS (
  SELECT * FROM VALUES
    ('NDAQ', 'Exchange operator'), ('ICE', 'Exchange operator'), ('CME', 'Exchange operator'), ('CBOE', 'Exchange operator'),
    ('SPY', 'Benchmark ETF'), ('QQQ', 'Benchmark ETF'), ('EWC', 'Benchmark ETF'),
    ('RY', 'Canadian interlisted'), ('TD', 'Canadian interlisted'), ('BMO', 'Canadian interlisted'),
    ('BNS', 'Canadian interlisted'), ('ENB', 'Canadian interlisted'), ('CNQ', 'Canadian interlisted'),
    ('SHOP', 'Canadian interlisted')
), px AS (
  SELECT p.ticker, t.grp, p.date, p.value AS adj_close
  FROM {P} p JOIN tickers t ON t.ticker = p.ticker
  WHERE p.variable = 'post-market_close_adjusted'
    AND p.date BETWEEN '2026-01-02' AND '2026-06-30'
)
SELECT ticker, grp, MIN(date) AS first_date, MAX(date) AS last_date, COUNT(*) AS trading_days,
       ROUND(100 * (MAX_BY(adj_close, date) / MIN_BY(adj_close, date) - 1), 2) AS h1_return_pct
FROM px
GROUP BY ticker, grp
ORDER BY h1_return_pct DESC;
```

**Largest daily move: `LAG`, drop the first day, then `QUALIFY`**
```sql
WITH px AS (
  SELECT ticker, date, value AS adj_close,
         LAG(value) OVER (PARTITION BY ticker ORDER BY date) AS prev_close
  FROM {P}
  WHERE variable = 'post-market_close_adjusted'
    AND ticker IN ('NDAQ', 'ICE', 'CME', 'CBOE')
    AND date <= '2026-06-30'
)
SELECT ticker, date, ROUND(100 * (adj_close / prev_close - 1), 2) AS pct_change
FROM px
WHERE prev_close IS NOT NULL          -- 2026-01-02 has no earlier close in your table
QUALIFY ROW_NUMBER() OVER (PARTITION BY ticker
                           ORDER BY ABS(adj_close / prev_close - 1) DESC) = 1
ORDER BY ticker;
```

**The trap:** your table starts on 2026-01-02, so `LAG` returns `NULL` there. Snowflake sorts `NULL` **first** in a descending sort, so without the `prev_close IS NOT NULL` filter (or `DESC NULLS LAST`), every ticker's "largest move" is a blank on 2026-01-02. To measure 2026-01-02's own move you'd need the 2025-12-31 close, which you deliberately didn't copy.
""",
)

render_go_further()

render_prompt(
    "4.2",
    "How deep was the selloff?",
    f"""Using post-market_close_adjusted in {P}, compute the maximum drawdown from 2026-01-02 to 2026-06-30 (the largest percent fall from a running peak) for NDAQ, ICE, CME, CBOE and SPY, with the trough date. Explain the window function you used. Read-only.""",
    optional=True,
)

render_check(
    """
| Ticker | Max drawdown | Trough |
| --- | --- | --- |
| CBOE | −36.86% | 2026-06-29 |
| CME | −30.91% | 2026-06-29 |
| ICE | −29.50% | 2026-06-30 |
| NDAQ | −23.24% | 2026-06-29 |
| SPY | −9.27% | 2026-03-30 |

A running peak is `MAX(adj_close) OVER (PARTITION BY ticker ORDER BY date ROWS UNBOUNDED PRECEDING)`. All four exchange operators bottomed at the end of June, at 2.5 to 4 times SPY's drawdown, yet CBOE finished the half only 2.3% down. A single return number hides the path.
"""
)

render_prompt(
    "4.3",
    "Do exchange stocks move with the market?",
    f"""Compute the correlation of daily returns (post-market_close_adjusted) from 2026-01-02 to 2026-06-30 between SPY and each of NDAQ, ICE, CME, CBOE, QQQ and EWC, from {P}, with the number of days used. Sort by correlation. Interpret the result in two sentences. Read-only.""",
    optional=True,
)

render_check(
    """
| Ticker | Correlation with SPY | Days |
| --- | --- | --- |
| QQQ | 0.94 | 122 |
| EWC | 0.61 | 122 |
| NDAQ | 0.34 | 122 |
| ICE | 0.12 | 122 |
| CBOE | −0.07 | 122 |
| CME | −0.11 | 122 |

122 days, not 123: the first day has no previous close. The ETFs track the market. The exchange operators barely do, and CME and CBOE move slightly against it: their revenue rises with trading volume, which tends to jump when markets are stressed. Expect CoCo to state an explanation like this as a hypothesis, not a fact.
"""
)

render_key_concepts(
    [
        ("Window function", "A calculation across related rows (the *window*) that keeps every row, for example `LAG(value) OVER (PARTITION BY ticker ORDER BY date)`."),
        ("PARTITION BY / ORDER BY", "`PARTITION BY ticker` restarts the window for each ticker. `ORDER BY date` decides what *previous* means."),
        ("NULL ordering", "In Snowflake, `NULL` sorts last ascending and **first** descending, unless you say `NULLS FIRST` / `NULLS LAST`."),
        ("Return vs drawdown", "Return compares start and end. Drawdown is the worst fall from a peak along the way. Risk discussions need both."),
        ("Correlation", "From −1 to +1: how closely two daily return series move together. It describes co-movement, not cause."),
    ]
)

render_takeaways(
    [
        "Compared three groups of tickers with window functions through CoCo, without writing them yourself.",
        "Checked trading-day counts before trusting a return.",
        "Caught the first-day `NULL` edge case that comes from where your copy starts.",
    ]
)
