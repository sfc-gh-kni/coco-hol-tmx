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

render_header(6, "HTML report snapshot", "1:30–1:40 (10 min)", "A one-page report built from a query, saved privately in your workspace.")
require_context()

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
    "6.1",
    "Exchange operators vs benchmarks",
    f"""Create a one-page, self-contained HTML report titled "Exchange operators vs benchmarks, H1 2026". Query my Iceberg table {P} for adjusted-close (post-market_close_adjusted) returns from 2026-01-02 to 2026-06-30 for NDAQ, ICE, CME, CBOE, SPY, QQQ and EWC, with each ticker's group (exchange operator or benchmark ETF) and number of trading days. Show the query result before building the report. Include a small table, one inline bar chart, the window dates, and a caveat that this is lagged Snowflake Curated Data (Free) for US listings, not TSX data. Inline HTML/CSS only, with no external scripts or images. Save it to my workspace. Do not publish or share. Do not ask me further questions; use sensible defaults.""",
)

render_review(
    [
        "The query result CoCo shows **before** it builds the page matches exercise 4. That result is what gets frozen into the report.",
        f"The query reads **your** table, `{P}`, and every ticker has 123 trading days.",
        "The HTML has no `<script src=...>`, CDN links or remote images.",
        "CoCo **saves** the file but doesn't publish or share it.",
    ]
)

render_check(
    """
Takes about 1.5 minutes. The report should:

- be titled **Exchange operators vs benchmarks, H1 2026**;
- show **QQQ +20.30%, SPY +9.90%, EWC +6.86%, CBOE −2.30%, CME −15.67%, NDAQ −18.26%, ICE −22.82%**;
- give the window **2026-01-02 to 2026-06-30**;
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
| Full table name | The report chat is a new conversation. It can't see your SQL file or earlier chats. |
| *Group and trading days* | Lets you see at a glance that every ticker covers the full window, so the comparison is fair. |
| *Show the query result before building* | Lets you check the numbers **before** they're frozen into a page. |
| Table + one chart + window + caveat | A clear, testable spec, so everyone's report is checkable against the same answers. |
| *Inline HTML/CSS only* | The file renders without internet access and can't load outside code. |
| *Do not publish or share* | Keeps the data snapshot private. |
| *Do not ask me further questions* | Skips the skill's scoping questions so the whole room stays in sync. |

The same structure works for any brief you'd normally build by hand: a weekly market note, a close-status page, a data-quality summary.
""",
)

render_go_further()

render_prompt(
    "6.2",
    "Add a risk section",
    f"""Add a second section to my report "Exchange operators vs benchmarks, H1 2026": a table of the maximum drawdown on adjusted close from 2026-01-02 to 2026-06-30, with its trough date, for NDAQ, ICE, CME, CBOE and SPY, from {P}. Show the query result first, keep everything inline, and add one sentence comparing the exchange operators with SPY. Do not publish or share. Do not ask me further questions.""",
    optional=True,
)

render_check(
    "CBOE **−36.86%**, CME **−30.91%**, ICE **−29.50%**, NDAQ **−23.24%** (all at the end of June 2026), SPY **−9.27%** on 2026-03-30. These match prompt 4.2."
)

render_key_concepts(
    [
        ("Self-contained HTML", "All styles, data and charts are inside the one file: no external scripts, fonts or images. It's portable and safe to preview."),
        ("Snapshot vs live", "A report is a point-in-time copy of query results. An app (exercise 5) re-queries live data under its owner role. Choose based on who'll read it and how fresh it needs to be."),
        ("Skill", "A packaged set of instructions CoCo loads for a task type. Here `html-authoring`; earlier, SQL authoring and Streamlit-in-Workspaces skills did the work."),
    ]
)

render_takeaways(
    [
        "Produced a report from a governed query over your own Iceberg table, and kept it private.",
        "Checked the report's numbers against exercise 4.",
    ]
)
