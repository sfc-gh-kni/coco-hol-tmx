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

render_header(3, "Compare trends", "0:55–1:05 (10 min)", "Use window functions to compare returns and find the biggest moves.")

st.info(
    "If it's already past 1:05, skip to **4. Build and deploy an app**. You can come back to this later.",
    icon=":material/timer:",
)

render_tools(
    [
        {"name": "Window functions", "icon": "functions", "description": "`LAG`, running `MAX` and `ROW_NUMBER` compare each row with its neighbours without a self-join."},
        {"name": "QUALIFY", "icon": "rule", "description": "Snowflake's filter on window-function results: the window-function equivalent of `HAVING`."},
        {"name": "MIN_BY / MAX_BY", "icon": "calculate", "description": "Return the value at the earliest or latest date in one pass: the first and last close of a period."},
    ]
)

render_prompt(
    "3.1",
    "2026 YTD returns and largest daily moves",
    """Using post-market_close_adjusted, compute each watchlist ticker's return from its first 2026 trading day to the latest available date, with segment, first and last date. Sort by return descending. Then, for the four exchange operators only, find each one's largest single-day percent move in 2026 using a window function, and explain how you handled the first day of the year.""",
)

render_review(
    [
        "The query uses `post-market_close_adjusted`, not the raw close.",
        "For the daily moves, the data pulled includes **late 2025**, so `LAG` has a previous close on 2026-01-02.",
        "The largest move is ranked by **absolute** change, so big drops count as well as big gains.",
    ]
)

render_check(
    """
Window: **2026-01-02 to 2026-08-12**.

| Segment | 2026 YTD return (adjusted close) |
| --- | --- |
| Canadian interlisted | CNQ +41.17%, BMO +41.09%, TD +33.29%, RY +27.67%, BNS +24.95%, ENB +10.03%, SHOP −4.44% |
| Exchange operator | CBOE +18.13%, CME +0.09%, NDAQ −0.58%, ICE −4.87% |
| Benchmark ETF | QQQ +18.06%, EWC +14.52%, SPY +13.73% |

Largest single-day moves in 2026:

| Ticker | Move | Date |
| --- | --- | --- |
| NDAQ | −9.69% | 2026-02-03 |
| CBOE | −9.61% | 2026-06-16 |
| ICE | −7.49% | 2026-02-11 |
| CME | −5.80% | 2026-06-01 |

On the first trading day of 2026, the previous close must come from **December 2025**, not be NULL.
"""
)

render_learn(
    "What this prompt does",
    """
**Returns: first and last value per ticker**
```sql
WITH px AS (
  SELECT ticker, date, value AS adj_close
  FROM TMX_COCO_HOL.SOURCE.STOCK_PRICE_TIMESERIES
  WHERE variable = 'post-market_close_adjusted' AND date >= '2026-01-01'
), ends AS (
  SELECT ticker,
         MIN_BY(adj_close, date) AS first_close, MIN(date) AS first_date,
         MAX_BY(adj_close, date) AS last_close,  MAX(date) AS last_date
  FROM px GROUP BY ticker
)
SELECT e.ticker, w.segment, e.first_date, e.last_date,
       ROUND(100 * (e.last_close / e.first_close - 1), 2) AS ytd_return_pct
FROM ends e JOIN TMX_COCO_HOL.SOURCE.WATCHLIST w USING (ticker)
ORDER BY ytd_return_pct DESC;
```

**Largest daily move: `LAG`, then `QUALIFY`**
```sql
WITH px AS (
  SELECT ticker, date, value AS adj_close,
         LAG(value) OVER (PARTITION BY ticker ORDER BY date) AS prev_close
  FROM TMX_COCO_HOL.SOURCE.STOCK_PRICE_TIMESERIES
  WHERE variable = 'post-market_close_adjusted'
    AND ticker IN ('NDAQ', 'ICE', 'CME', 'CBOE')
    AND date >= '2025-12-01'          -- reach back so 2026-01-02 has a prior close
)
SELECT ticker, date, ROUND(100 * (adj_close / prev_close - 1), 2) AS pct_change
FROM px
WHERE date >= '2026-01-01'
QUALIFY ROW_NUMBER() OVER (PARTITION BY ticker
                           ORDER BY ABS(adj_close / prev_close - 1) DESC) = 1
ORDER BY ticker;
```

The `2025-12-01` lower bound is the edge case the prompt asks about. Filter to 2026 **before** the `LAG` and the first day of the year gets a NULL previous close.
""",
)

render_go_further()

render_prompt(
    "3.2",
    "How deep was the selloff?",
    """Using post-market_close_adjusted in TMX_COCO_HOL.SOURCE.STOCK_PRICE_TIMESERIES, compute the maximum drawdown in 2026 (the largest percent fall from a running peak) for NDAQ, ICE, CME, CBOE and SPY, with the trough date. Explain the window function you used. Read-only.""",
    optional=True,
)

render_check(
    """
| Ticker | Max drawdown 2026 | Trough |
| --- | --- | --- |
| CBOE | −36.86% | 2026-06-29 |
| CME | −30.91% | 2026-06-29 |
| ICE | −29.50% | 2026-06-30 |
| NDAQ | −23.24% | 2026-06-29 |
| SPY | −9.27% | 2026-03-30 |

A running peak is `MAX(adj_close) OVER (PARTITION BY ticker ORDER BY date ROWS UNBOUNDED PRECEDING)`. All four exchange operators bottomed at the end of June, at 2.5 to 4 times SPY's drawdown, yet CBOE still ended the period up 18%. A single return number hides the path.
"""
)

render_prompt(
    "3.3",
    "Do exchange stocks move with the market?",
    """Compute the correlation of 2026 daily returns (post-market_close_adjusted) between SPY and each of NDAQ, ICE, CME, CBOE, QQQ and EWC from TMX_COCO_HOL.SOURCE.STOCK_PRICE_TIMESERIES, with the number of days used. Sort by correlation. Interpret the result in two sentences. Read-only.""",
    optional=True,
)

render_check(
    """
| Ticker | Correlation with SPY | Days |
| --- | --- | --- |
| QQQ | 0.93 | 153 |
| EWC | 0.60 | 153 |
| NDAQ | 0.28 | 153 |
| ICE | 0.07 | 153 |
| CBOE | −0.14 | 153 |
| CME | −0.16 | 153 |

The ETFs track the market. The exchange operators barely do, and CME and CBOE move slightly against it: their revenue rises with trading volume, which tends to jump when markets are stressed. Expect CoCo to state an explanation like this as a hypothesis, not a fact.
"""
)

render_key_concepts(
    [
        ("Window function", "A calculation across related rows (the *window*) that keeps every row, for example `LAG(value) OVER (PARTITION BY ticker ORDER BY date)`."),
        ("PARTITION BY / ORDER BY", "`PARTITION BY ticker` restarts the window for each ticker. `ORDER BY date` decides what *previous* means."),
        ("Return vs drawdown", "Return compares start and end. Drawdown is the worst fall from a peak along the way. Risk discussions need both."),
        ("Correlation", "From −1 to +1: how closely two daily return series move together. It describes co-movement, not cause."),
    ]
)

render_takeaways(
    [
        "Used `LAG` and window functions through CoCo without writing them yourself.",
        "Checked an edge case (the first day of the year) instead of trusting the output.",
    ]
)
