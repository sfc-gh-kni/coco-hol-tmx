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

render_header(2, "Generate and validate SQL", "0:35–0:55 (20 min)", "Get CoCo to write a query, then prove it's right.")

render_tools(
    [
        {"name": "CoCo SQL authoring", "icon": "code", "description": "CoCo drafts SQL from your description, writes it into the open file as a reviewable change, and runs it only when you approve."},
        {"name": "Undo / Keep diffs", "icon": "sync_alt", "description": "File edits arrive as a highlighted change. Keep accepts it into your file; Undo throws it away."},
        {"name": "TMX_HOL_WH", "icon": "memory", "description": "The shared lab warehouse that runs your queries. It suspends itself after 60 seconds idle."},
    ]
)

st.markdown(
    """
Generated SQL is a draft, not an answer. This exercise practises the loop you'll use on real work: **describe, review, run, then prove**. The source table is in long format, so the first job is a pivot to one row per ticker and day.
"""
)

render_prompt(
    "2.1",
    "Pivot and summarize the exchange operators",
    """Write a read-only query that pivots TMX_COCO_HOL.SOURCE.STOCK_PRICE_TIMESERIES to one row per ticker and date, with columns for close (post-market_close) and nasdaq_volume, for the exchange operators NDAQ, ICE, CME and CBOE from 2026-04-01 to 2026-06-30. Then summarize per ticker: trading days, distinct dates, missing closes, average Nasdaq volume, and min/max close. Use fully qualified names and show the SQL before running it.""",
)

st.markdown(
    """
CoCo usually writes the SQL **into your open SQL file** as a change you can review, and may rename the file to match. Click **Keep** to accept it, then run it after you've read it.
"""
)

render_review(
    [
        "The `WHERE` clause limits `VARIABLE` to `post-market_close` and `nasdaq_volume`.",
        "Dates use `BETWEEN '2026-04-01' AND '2026-06-30'`, or `>=` and `<=`, so both ends are included.",
        "The pivot groups by **ticker and date** before the summary aggregates.",
        "Raw close is fine here: this is a price range, not a return.",
    ]
)

render_check(
    """
Each ticker: **62 trading days, 62 distinct dates, 0 missing closes**.

| Ticker | Avg Nasdaq volume | Min close | Max close |
| --- | --- | --- | --- |
| CBOE | 171,237 | 231.21 | 366.94 |
| CME | 1,137,952 | 219.65 | 314.00 |
| ICE | 322,316 | 122.80 | 167.79 |
| NDAQ | 1,487,524 | 76.99 | 92.73 |

CBOE's wide range is real: the stock sold off from late May through June 2026. It isn't a duplicate-row bug.
"""
)

render_learn(
    "What this prompt does",
    """
There are two common ways to turn long format into wide. CoCo may use either.

**Conditional aggregation**, which is portable and easy to read:
```sql
WITH daily AS (
  SELECT ticker, date,
         MAX(IFF(variable = 'post-market_close', value, NULL)) AS close_usd,
         MAX(IFF(variable = 'nasdaq_volume',     value, NULL)) AS nasdaq_volume
  FROM TMX_COCO_HOL.SOURCE.STOCK_PRICE_TIMESERIES
  WHERE ticker IN ('NDAQ', 'ICE', 'CME', 'CBOE')
    AND date BETWEEN '2026-04-01' AND '2026-06-30'
    AND variable IN ('post-market_close', 'nasdaq_volume')
  GROUP BY ticker, date
)
SELECT ticker,
       COUNT(*)                   AS trading_days,
       COUNT(DISTINCT date)       AS distinct_days,
       COUNT_IF(close_usd IS NULL) AS missing_close,
       ROUND(AVG(nasdaq_volume))  AS avg_nasdaq_volume,
       ROUND(MIN(close_usd), 2)   AS min_close,
       ROUND(MAX(close_usd), 2)   AS max_close
FROM daily
GROUP BY ticker
ORDER BY ticker;
```

**Snowflake `PIVOT`**, which is shorter. Note the quoted column names it produces:
```sql
SELECT *
FROM (
  SELECT ticker, date, variable, value
  FROM TMX_COCO_HOL.SOURCE.STOCK_PRICE_TIMESERIES
  WHERE ticker = 'NDAQ' AND date BETWEEN '2026-06-24' AND '2026-06-30'
    AND variable IN ('post-market_close', 'nasdaq_volume')
)
PIVOT (MAX(value) FOR variable IN ('post-market_close', 'nasdaq_volume'))
ORDER BY date;
```

`trading_days` equal to `distinct_days` is your first sign that the pivot didn't duplicate rows. Prompt 2.2 makes that check explicit.
""",
)

render_prompt(
    "2.2",
    "Prove the pivot is correct",
    """Prove there is exactly one row per ticker and date in your pivot, and that no date outside the requested window is included. Show the check query.""",
)

render_check(
    """
CoCo should show a check query that returns **no duplicate ticker/date pairs** and **no dates before 2026-04-01 or after 2026-06-30**. Typical patterns: `GROUP BY ticker, date HAVING COUNT(*) > 1` returning zero rows, and `MIN(date)` / `MAX(date)` per ticker.

Notice that this prompt doesn't repeat the table name or tickers. In the same conversation, CoCo carries that context forward.
"""
)

render_go_further()

render_prompt(
    "2.3",
    "Save the pivot as your own view",
    """Create a view named TMX_COCO_HOL.LAB.<MY_INITIALS>_EXCH_OPS_Q2 (replace <MY_INITIALS> with my initials) from the pivot query, with columns ticker, date, close and nasdaq_volume. Show the CREATE VIEW statement before running it. Then count its rows, distinct tickers and min/max date. Do not create or change anything else.""",
    optional=True,
)

st.caption(
    "Replace `<MY_INITIALS>` before you send it. The LAB schema is shared, so a unique name keeps you from overwriting a neighbour's view."
)

render_check(
    """
**248 rows** (4 tickers × 62 days), **4 tickers**, **2026-04-01 to 2026-06-30**.

This is the only prompt in exercises 1–3 that creates an object. Check that the statement is `CREATE VIEW` (or `CREATE OR REPLACE VIEW`) **in `TMX_COCO_HOL.LAB`** with **your** name, never in `SOURCE`. The lab role can't write to `SOURCE`, so if CoCo tries, it gets a privilege error.
"""
)

render_prompt(
    "2.4",
    "Monthly volume trend",
    """Using TMX_COCO_HOL.SOURCE.STOCK_PRICE_TIMESERIES, show average daily nasdaq_volume per month for NDAQ, ICE, CME and CBOE from April to June 2026, one row per ticker and month. Which month stands out, and what might explain it? Read-only.""",
    optional=True,
)

render_check(
    """
| Ticker | Apr 2026 | May 2026 | Jun 2026 |
| --- | --- | --- | --- |
| CBOE | 93,292 | 126,761 | 291,540 |
| CME | 867,769 | 910,665 | 1,624,598 |
| ICE | 250,328 | 278,795 | 435,751 |
| NDAQ | 1,210,412 | 1,285,628 | 1,956,917 |

**June** stands out for all four: volume was 62% (NDAQ) to 212% (CBOE) above April. That lines up with the June selloff you'll measure in exercise 3. CoCo can point out the timing, but it can't know the cause from this data alone. A good answer says so.
"""
)

render_key_concepts(
    [
        ("Grain", "What one row represents. The source grain is *ticker × date × variable*. After the pivot it's *ticker × date*. Most wrong answers come from aggregating at the wrong grain."),
        ("Conditional aggregation", "`MAX(IFF(variable = 'x', value, NULL))` inside a `GROUP BY` picks one measure per group, turning rows into columns."),
        ("CTE (`WITH` clause)", "A named intermediate result. CoCo uses CTEs to make multi-step SQL readable: pivot first, then summarize."),
        ("Validation query", "A second, independent query that tests an assumption, such as uniqueness, the date window or null counts. Cheap to run, and it catches most generated-SQL mistakes."),
    ]
)

render_takeaways(
    [
        "Turned a business question into reviewed, runnable SQL.",
        "Accepted CoCo's change only after reading it.",
        "Validated the grain and the date window with a separate check query.",
    ]
)
