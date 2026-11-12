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

render_header(5, "HTML report snapshot", "1:30–1:40 (10 min)", "A one-page report built from a query, saved privately in your workspace.")

render_tools(
    [
        {"name": "HTML reports", "icon": "html", "description": "Self-contained `.html` files in your workspace that preview in Snowsight. Good for a one-page brief you'd otherwise build in slides."},
        {"name": "html-authoring skill", "icon": "psychology", "description": "The CoCo skill behind **+ Add new → Report**. It scopes the report, runs the query and writes the page."},
        {"name": "Result snapshot", "icon": "visibility", "description": "The report embeds the numbers at build time. It doesn't re-query, so it can go stale, and anyone it's shared with can see them."},
    ]
)

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

render_review(
    [
        "The query result CoCo shows **before** it builds the page matches exercise 3. That result is what gets frozen into the report.",
        "The HTML has no `<script src=...>`, CDN links or remote images.",
        "CoCo **saves** the file but doesn't publish or share it.",
    ]
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
    "What this prompt does, and why it's worded this way",
    """
| Part of the prompt | Why it's there |
| --- | --- |
| Full table names | The report chat is a new conversation. It can't see your SQL file or earlier chats. |
| *Show the query result before building* | Lets you check the numbers **before** they're frozen into a page. |
| Table + one chart + as-of date + caveat | A clear, testable spec, so everyone's report is checkable against the same answers. |
| *Inline HTML/CSS only* | The file renders without internet access and can't load outside code. |
| *Do not publish or share* | Keeps the data snapshot private. |
| *Do not ask me further questions* | Skips the skill's scoping questions so 100 people stay in sync. |

The same structure works for any brief you'd normally build by hand: a weekly market note, a close-status page, a data-quality summary.
""",
)

render_go_further()

render_prompt(
    "5.2",
    "Add a risk section",
    """Add a second section to my report "Exchange operators vs benchmarks, 2026 YTD": a table of each ticker's maximum 2026 drawdown on adjusted close with its trough date, for NDAQ, ICE, CME, CBOE and SPY, from TMX_COCO_HOL.SOURCE.STOCK_PRICE_TIMESERIES. Show the query result first, keep everything inline, and add one sentence comparing the exchange operators with SPY. Do not publish or share. Do not ask me further questions.""",
    optional=True,
)

render_check(
    "CBOE **−36.86%**, CME **−30.91%**, ICE **−29.50%**, NDAQ **−23.24%** (all at the end of June 2026), SPY **−9.27%** on 2026-03-30. These match prompt 3.2."
)

render_key_concepts(
    [
        ("Self-contained HTML", "All styles, data and charts are inside the one file: no external scripts, fonts or images. It's portable and safe to preview."),
        ("Snapshot vs live", "A report is a point-in-time copy of query results. An app (exercise 4) re-queries live data under its owner role. Choose based on who'll read it and how fresh it needs to be."),
        ("Skill", "A packaged set of instructions CoCo loads for a task type. Here `html-authoring`; earlier, SQL authoring and Streamlit-in-Workspaces skills did the work."),
    ]
)

render_takeaways(
    [
        "Produced a report from a governed query, and kept it private.",
        "Checked the report's numbers against exercise 3.",
    ]
)
