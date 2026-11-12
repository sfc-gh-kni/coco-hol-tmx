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

render_header(4, "Compare trends", "0:55–1:05 (10 min)", "Rank the S&P 500 on first-half returns and find the biggest moves, with window functions.")
require_context()

st.info(
    "If it's already past 1:05, skip to **5. Build and deploy an app**. You can come back to this later.",
    icon=":material/timer:",
)

render_tools(
    [
        {"name": "Window functions", "icon": "functions", "description": "`LAG`, running `MAX` and `RANK` compare each row with its neighbours without a self-join."},
        {"name": "QUALIFY", "icon": "rule", "description": "Snowflake's filter on window-function results: the window-function equivalent of `HAVING`."},
        {"name": "MIN_BY / MAX_BY", "icon": "calculate", "description": "Return the value at the earliest or latest date in one pass: the first and last close of a period."},
    ]
)

st.markdown(
    "The window is fixed at **2026-01-02 to 2026-06-30** (the first half), so your answers match the guide whenever you copied the data."
)

render_prompt(
    "4.1",
    "First-half returns and largest daily moves",
    f"""Using post-market_close_adjusted in {P}, compute each ticker's return from 2026-01-02 to 2026-06-30. Only rank tickers that have a close on every trading day in that window, and list the tickers you excluded. Show the top 5 and bottom 5 returns, the median and average return, how many tickers rose, and the rank of NDAQ, ICE, CME and CBOE. Then, for those four exchange operators, find each one's largest single-day percent move in the same window using a window function, and explain how you handled the first trading day of 2026.""",
)

render_review(
    [
        "The query uses `post-market_close_adjusted`, not the raw close.",
        "Tickers without all **123** trading days are excluded **before** ranking: BNY, MRSH and ECHO (exercise 2.2).",
        "The largest move is ranked by **absolute** change, so big drops count as well as big gains.",
        "Rows whose previous close is `NULL` are filtered out before ranking the moves.",
    ]
)

render_check(
    """
**500 tickers ranked**; excluded **BNY, MRSH, ECHO**. Median **+7.32%**, average **+12.55%**, **312 of 500** rose.

| Top 5 | Return | Bottom 5 | Return |
| --- | --- | --- | --- |
| SNDK | +709.61% | EPAM | −59.97% |
| MU | +262.70% | INTU | −58.24% |
| INTC | +252.89% | CSGP | −56.98% |
| WDC | +241.01% | BSX | −54.89% |
| DELL | +239.17% | TTD | −52.16% |

| Exchange operator | Return | Rank of 500 |
| --- | --- | --- |
| CBOE | −2.30% | 326 |
| CME | −15.67% | 413 |
| NDAQ | −18.26% | 430 |
| ICE | −22.82% | 448 |

Largest single-day moves:

| Ticker | Move | Date |
| --- | --- | --- |
| NDAQ | −9.69% | 2026-02-03 |
| CBOE | −9.61% | 2026-06-16 |
| ICE | −7.49% | 2026-02-11 |
| CME | −5.80% | 2026-06-01 |

**If BNY tops the list at +1,369%**, the completeness filter is missing: that's the reused-ticker jump from exercise 2. **If every move is dated 2026-01-02 with a blank value**, the `NULL` previous close wasn't filtered (see below).
"""
)

render_learn(
    "What this prompt does, and the first-day trap",
    f"""
**Returns: completeness filter, then first and last value per ticker**
```sql
WITH px AS (
  SELECT ticker, date, value AS adj_close
  FROM {P}
  WHERE variable = 'post-market_close_adjusted'
    AND date BETWEEN '2026-01-02' AND '2026-06-30'
), complete AS (
  SELECT ticker FROM px GROUP BY ticker
  HAVING COUNT(DISTINCT date) = (SELECT COUNT(DISTINCT date) FROM px)   -- 123
), ret AS (
  SELECT ticker,
         ROUND(100 * (MAX_BY(adj_close, date) / MIN_BY(adj_close, date) - 1), 2) AS h1_return_pct
  FROM px WHERE ticker IN (SELECT ticker FROM complete)
  GROUP BY ticker
)
SELECT ticker, h1_return_pct, RANK() OVER (ORDER BY h1_return_pct DESC) AS rank_of_500
FROM ret
ORDER BY rank_of_500;
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
    f"""Using post-market_close_adjusted in {P}, compute the maximum drawdown from 2026-01-02 to 2026-06-30 (the largest percent fall from a running peak) for NDAQ, ICE, CME and CBOE, with the trough date. Then give the median maximum drawdown across all tickers that have a close on every trading day in that window. Explain the window function you used. Read-only.""",
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
| Median S&P 500 stock (500 tickers) | −21.01% | |

A running peak is `MAX(adj_close) OVER (PARTITION BY ticker ORDER BY date ROWS UNBOUNDED PRECEDING)`. All four exchange operators bottomed at the end of June, deeper than the typical S&P 500 stock, yet CBOE finished the half only 2.3% down. A single return number hides the path.
"""
)

render_prompt(
    "4.3",
    "Do exchange stocks move with the market?",
    f"""From {P}, build an equal-weight S&P 500 daily return series: on each trading day from 2026-01-02 to 2026-06-30, the average daily return (post-market_close_adjusted) of the tickers that have a close on every trading day in that window. Compute the correlation of NDAQ, ICE, CME and CBOE's daily returns with that series, with the number of days used, sorted by correlation. Interpret the result in two sentences. Read-only.""",
    optional=True,
)

render_check(
    """
| Ticker | Correlation with the equal-weight S&P 500 | Days |
| --- | --- | --- |
| NDAQ | 0.37 | 122 |
| ICE | 0.22 | 122 |
| CBOE | −0.03 | 122 |
| CME | −0.04 | 122 |

122 days, not 123: the first day has no previous close. NDAQ and ICE move modestly with the market; CME and CBOE barely do. Their revenue rises with trading volume, which tends to jump when markets are stressed. Expect CoCo to state an explanation like this as a hypothesis, not a fact.

Compounding the equal-weight daily average gives **+10.30%** for the half: a benchmark line you can add to your app in exercise 5.
"""
)

render_key_concepts(
    [
        ("Window function", "A calculation across related rows (the *window*) that keeps every row, for example `LAG(value) OVER (PARTITION BY ticker ORDER BY date)`."),
        ("PARTITION BY / ORDER BY", "`PARTITION BY ticker` restarts the window for each ticker. `ORDER BY date` decides what *previous* means."),
        ("NULL ordering", "In Snowflake, `NULL` sorts last ascending and **first** descending, unless you say `NULLS FIRST` / `NULLS LAST`."),
        ("Return vs drawdown", "Return compares start and end. Drawdown is the worst fall from a peak along the way. Risk discussions need both."),
        ("Equal-weight index", "Each stock counts the same, whatever its size. The official S&P 500 is cap-weighted, so its return differs."),
    ]
)

render_takeaways(
    [
        "Ranked 500 stocks with window functions through CoCo, without writing them yourself.",
        "Excluded incomplete tickers before ranking, instead of trusting the output.",
        "Caught the first-day `NULL` edge case that comes from where your copy starts.",
    ]
)
