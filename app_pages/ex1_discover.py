import streamlit as st

from components import render_check, render_header, render_learn, render_prompt, render_takeaways

render_header(1, "Discover the data", "0:20–0:35 (15 min)", "Know what's in the tables, and what isn't, before you trust a number.")

render_prompt(
    "1.1",
    "Segments, freshness and caveats",
    """Using TMX_COCO_HOL.SOURCE.WATCHLIST, list the tickers by segment. Then tell me the latest available date in TMX_COCO_HOL.SOURCE.STOCK_PRICE_TIMESERIES and explain why it is not today. Explain the difference between post-market_close and post-market_close_adjusted, and what nasdaq_volume does and does not measure. Read-only.""",
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

st.markdown("##### Try one of your own")
st.markdown(
    """
Ask a follow-up in your own words. Ideas:
- *Which ticker has the most rows, and are any dates missing for it?*
- *What do PRIMARY_EXCHANGE_CODE and ASSET_CLASS contain for the ETFs?*
"""
)

render_learn(
    "Why start with discovery?",
    """
CoCo answers from your data, under **your** role. Asking it first what the data is, how fresh it is and what each column measures catches the mistakes that are easy to make in market data:

- comparing raw closes across a dividend date;
- calling Nasdaq-venue volume "total volume";
- assuming "latest" means today.
""",
)

render_takeaways(
    [
        "Grounded CoCo in real tables using fully qualified names.",
        "Confirmed freshness, grain and the meaning of each measure.",
        "Kept CoCo read-only by saying so in the prompt and checking each SQL approval.",
    ]
)
