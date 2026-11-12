import streamlit as st

from components import render_check, render_header, render_learn, render_prompt, render_takeaways

render_header(5, "HTML report snapshot", "1:30–1:40 (10 min)", "A one-page report built from a query, saved privately in your workspace.")

st.markdown(
    """
**+ Add new → Report** doesn't create an empty file. It opens a CoCo chat that asks three scoping questions first. To stay in step with everyone:

1. Choose **+ Add new → Report** in My Workspace, then click **Cancel questions**. You can also use any new CoCo chat.
2. Paste the prompt below. It ends with *do not ask me further questions*, so CoCo runs straight through.
3. Approve the query when CoCo shows it, then open the saved `.html` file to preview it.
"""
)

render_prompt(
    "5.1",
    "Exchange operators vs benchmarks",
    """Create a one-page, self-contained HTML report titled "Exchange operators vs benchmarks, 2026 YTD". Query TMX_COCO_HOL.SOURCE.STOCK_PRICE_TIMESERIES and TMX_COCO_HOL.SOURCE.WATCHLIST for adjusted-close returns from the first 2026 trading day to the latest available date for NDAQ, ICE, CME, CBOE, SPY, QQQ and EWC, and show the query result before building the report. Include a small table, one inline chart, the as-of date, and a caveat that this is lagged Snowflake Curated Data (Free) for US listings, not TSX data. Inline HTML/CSS only, with no external scripts or images. Save it to my workspace. Do not publish or share. Do not ask me further questions; use sensible defaults.""",
)

render_check(
    """
Takes about 1.5 minutes. The report should:

- be titled **Exchange operators vs benchmarks, 2026 YTD**;
- show **CBOE +18.13%, QQQ +18.06%, EWC +14.52%, SPY +13.73%, CME +0.09%, NDAQ −0.58%, ICE −4.87%**;
- give the as-of date **2026-08-12**;
- include the caveat about lagged free data for US listings, not TSX data.
"""
)

st.warning(
    "An HTML report stores a **snapshot of the query results**. Anyone you share it with can see those numbers without access to the tables. Leave yours unpublished.",
    title="Don't publish or share the report",
    icon=":material/lock:",
)

render_learn(
    "Why use full table names here?",
    "The report chat is a separate conversation. It can't see your SQL file or earlier chats, so every prompt needs fully qualified names.",
)

render_takeaways(
    [
        "Produced a report from a governed query, and kept it private.",
        "Checked the report's numbers against exercise 3.",
    ]
)
