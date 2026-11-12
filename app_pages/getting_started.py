import streamlit as st

from components import (
    PRICES,
    ROLE,
    WAREHOUSE,
    render_check,
    render_header,
    render_learn,
    render_prompt,
)

render_header(0, "Get started", "0:10–0:20 (10 min)", "Signed in, right role and warehouse, CoCo answering.")

st.markdown("#### 1. Sign in")
st.markdown(
    f"""
1. Open the **Snowsight link** your facilitator posts in the meeting chat.
2. Sign in with **your own** TMX login. Never share a login or sign in as someone else.
3. Open the user menu (your name or initials, bottom left) and switch your role to **`{ROLE}`**.
"""
)

st.markdown("#### 2. Open your workspace and a SQL file")
st.markdown(
    f"""
1. Go to **Projects → Workspaces** and open **My Workspace**. Files here are private to you.
2. Choose **+ Add new → SQL file**.
3. In the context selector above the editor, check that the role is **`{ROLE}`** and pick the warehouse **`{WAREHOUSE}`**.
4. Open the **Cortex Code (CoCo) side panel** beside the file. Keep the default model (Auto) and leave tool approvals **on**.
"""
)

st.info(
    "Keep this SQL file open for exercises 1–3. CoCo uses the open file as context and may write SQL straight into it.",
    icon=":material/lightbulb:",
)

st.markdown("#### 3. Smoke test")

render_prompt(
    "0.1",
    "Can CoCo see the lab data?",
    """I am rehearsing a read-only hands-on lab. With my current role, describe the tables in TMX_COCO_HOL.SOURCE: their grain, key columns, the distinct values of VARIABLE, the date range and the number of tickers. Do not create, alter or drop objects. Cite the fully qualified table names you used.""",
)

st.markdown(
    "CoCo shows the SQL it wants to run and waits. **Read it, then approve.** It should be `SELECT` or `DESCRIBE` only."
)

render_check(
    f"""
- Two tables: `{PRICES}` and `TMX_COCO_HOL.SOURCE.WATCHLIST`.
- **Long format**: one row per ticker, date and variable.
- **9 variables**: open, high, low and close (each raw and adjusted), plus `nasdaq_volume`.
- **14 tickers**, **2024-01-02 to 2026-08-12**, **82,404 rows** (654 trading days).

Takes about 1 minute.
"""
)

render_learn(
    "Nothing happens, or CoCo says it can't find the tables",
    f"""
- Check the role at the top of the CoCo panel and the SQL file: it must be `{ROLE}`.
- Check the warehouse is `{WAREHOUSE}`.
- If CoCo isn't offered at all, raise your hand in the meeting chat. The facilitator checks your role and CoCo access.

See **Troubleshooting** in the sidebar for more.
""",
)
