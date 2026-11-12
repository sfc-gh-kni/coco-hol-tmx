import streamlit as st

from components import render_check, render_header, render_learn, render_prompt, render_takeaways

render_header(3, "Compare trends", "0:55–1:05 (10 min)", "Use window functions to compare returns and find the biggest moves.")

st.info(
    "If it's already past 1:05, skip to **4. Build and deploy an app**. You can come back to this later.",
    icon=":material/timer:",
)

render_prompt(
    "3.1",
    "2026 YTD returns and largest daily moves",
    """Using post-market_close_adjusted, compute each watchlist ticker's return from its first 2026 trading day to the latest available date, with segment, first and last date. Sort by return descending. Then, for the four exchange operators only, find each one's largest single-day percent move in 2026 using a window function, and explain how you handled the first day of the year.""",
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
    "Why adjusted close?",
    """
Raw closes drop on ex-dividend dates even though holders didn't lose money. Adjusted closes correct for dividends and splits, so returns compare fairly. That matters for the banks and Enbridge in the watchlist, which all pay dividends.
""",
)

render_takeaways(
    [
        "Used `LAG` and window functions through CoCo without writing them yourself.",
        "Checked an edge case (the first day of the year) instead of trusting the output.",
    ]
)
