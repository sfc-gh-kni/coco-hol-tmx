import streamlit as st

from components import render_check, render_header, render_learn, render_prompt, render_takeaways

render_header(2, "Generate and validate SQL", "0:35–0:55 (20 min)", "Get CoCo to write a query, then prove it's right.")

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

render_prompt(
    "2.2",
    "Prove the pivot is correct",
    """Prove there is exactly one row per ticker and date in your pivot, and that no date outside the requested window is included. Show the check query.""",
)

render_check(
    """
CoCo should show a check query that returns **no duplicate ticker/date pairs** and **no dates before 2026-04-01 or after 2026-06-30**. Typical patterns: `GROUP BY ticker, date HAVING COUNT(*) > 1` returning zero rows, and `MIN(date)` / `MAX(date)` per ticker.
"""
)

render_learn(
    "Why the pivot matters",
    """
The source is **long format**: each ticker and date has up to 9 rows, one per variable. Aggregating it without pivoting or filtering on `VARIABLE` mixes prices and volumes and inflates counts. Asking CoCo to *prove* one row per ticker and date is a habit worth keeping for any generated SQL.
""",
)

render_takeaways(
    [
        "Turned a business question into reviewed, runnable SQL.",
        "Accepted CoCo's change only after reading it.",
        "Validated the grain and the date window with a separate check query.",
    ]
)
