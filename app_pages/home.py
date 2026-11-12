import streamlit as st

from components import PRICES, WATCHLIST

st.title("TMX CoCo hands-on lab")
st.markdown(
    "Use **Cortex Code (CoCo)** in Snowsight to explore market data, write and check SQL, "
    "and build and deploy your own Streamlit app. No local install is needed."
)

st.space("small")

with st.container(horizontal=True):
    st.metric("Hands-on", "90 min", border=True)
    st.metric("Exercises", "5", border=True)
    st.metric("You deploy", "1 app", border=True)
    st.metric("Tools", "Snowsight only", border=True)

st.space("small")

st.markdown("#### Agenda")
st.table(
    [
        {"Time": "0:00–0:10", "Block": "Welcome and intro (facilitator)"},
        {"Time": "0:10–0:20", "Block": "Get started: sign in, role, warehouse, CoCo panel, smoke test"},
        {"Time": "0:20–0:35", "Block": "Exercise 1: Discover the data"},
        {"Time": "0:35–0:55", "Block": "Exercise 2: Generate and validate SQL"},
        {"Time": "0:55–1:05", "Block": "Exercise 3: Compare trends (optional if you are behind)"},
        {"Time": "1:05–1:30", "Block": "Exercise 4: Build and deploy a Streamlit app"},
        {"Time": "1:30–1:40", "Block": "Exercise 5: HTML report snapshot"},
        {"Time": "1:40–2:00", "Block": "Q&A"},
    ],
    hide_index=True,
)
st.caption("There is no break. Exercise 4 is the one that matters most: if you fall behind, skip 3 and jump to 4 at 1:05.")

st.markdown("#### How this guide works")
st.markdown(
    """
- Each exercise has **numbered prompts**. Copy one, paste it into the **CoCo side panel** in Snowsight, and press Enter.
- CoCo asks before it runs SQL or changes a file. **Read what it proposes, then approve.** Reviewing is part of the lab.
- Open **Check your result** under a prompt to compare your numbers with the verified answers.
- Open **What this prompt does** to see the kind of SQL or code CoCo writes, and why.
- Use the **Before you approve** checklist on each exercise to practise reviewing CoCo's work.
- **Go further** prompts are optional, for when you're ahead. They have verified answers too.
- Tick **Done** to track your progress in the sidebar.
- CoCo's wording, SQL and layout will differ from your neighbour's. The **numbers** should match.
"""
)

st.markdown("#### What you'll build")
st.table(
    [
        {"Exercise": "Exercise 1", "You produce": "A data profile: segments, freshness, grain and caveats", "Skill practised": "Grounding CoCo in governed data"},
        {"Exercise": "Exercise 2", "You produce": "A validated pivot and summary query", "Skill practised": "Reviewing and proving generated SQL"},
        {"Exercise": "Exercise 3", "You produce": "2026 returns and the largest daily moves", "Skill practised": "Window functions and edge cases"},
        {"Exercise": "Exercise 4", "You produce": "A **deployed** Streamlit price explorer", "Skill practised": "Spec → plan → review → deploy"},
        {"Exercise": "Exercise 5", "You produce": "A private one-page HTML report", "Skill practised": "Turning a query into a brief, safely"},
    ],
    hide_index=True,
)

st.info(
    "New to CoCo? Read **Meet CoCo** in the sidebar before the session: it covers approvals, diffs, plans and how to write a good prompt.",
    icon=":material/smart_toy:",
)

st.markdown("#### The data")
with st.container(border=True):
    st.markdown(
        f"""
Daily stock prices and Nasdaq trading volumes from **Snowflake Curated Data (Free)**, copied into a read-only snapshot for this lab:

| Table | What it holds |
| --- | --- |
| `{PRICES}` | One row per ticker, date and variable (long format), 2024-01-02 to 2026-08-12 |
| `{WATCHLIST}` | 14 tickers grouped into three segments |

| Segment | Tickers |
| --- | --- |
| Exchange operator | NDAQ, ICE, CME, CBOE |
| Canadian interlisted | RY, TD, BMO, BNS, ENB, CNQ, SHOP |
| Benchmark ETF | SPY, QQQ, EWC |

Full column and variable details are in the **Data dictionary** page.
"""
    )

st.warning(
    "Prices are **US listings in USD**, and the free data lags by a few months. "
    "`nasdaq_volume` counts Nasdaq-venue trades only, not total market volume. "
    "This is **not TSX market data**.",
    title="Read before you analyze",
    icon=":material/warning:",
)

st.markdown("#### Ground rules")
st.markdown(
    """
- Everyone shares one lab role and one app schema. **Work only on your own files and app.** Don't drop, replace or edit anything you didn't create.
- The source tables are read-only. CoCo can't change them, and you don't need it to.
- Don't paste passwords, personal data or confidential TMX information into CoCo prompts or app code.
"""
)

st.space("small")
st.page_link("app_pages/getting_started.py", label="Next: get started", icon=":material/arrow_forward:")
