import streamlit as st

from components import (
    SOURCE_VIEW,
    ctx,
    render_check,
    render_header,
    render_learn,
    render_prompt,
    require_context,
)

c = ctx()

render_header(0, "Get started", "0:10–0:20 (10 min)", "Signed in, your team's context set, CoCo answering.")

with st.container(border=True):
    st.markdown("##### :material/checklist: Before the lab (the day before, if you can)")
    st.markdown(
        """
- Sign in to Snowsight once with your TMX login and finish any MFA setup. Sign-in problems are the most common cause of a slow start.
- Find out **which team you're on**. Your facilitator assigns teams.
- Use a current **Chrome, Edge or Firefox**. Allow pop-ups from Snowflake.
- Set up your screen with this guide on one side and Snowsight on the other, or use two monitors. You'll copy prompts across constantly.
- Read **Meet CoCo** in the sidebar (5 minutes).
"""
    )

st.markdown("#### 1. Tell this guide who you are")
st.markdown(
    """
In the sidebar, under **Your lab context**:

1. Pick **your team**.
2. Enter **your initials**, for example `KN`. If a teammate has the same initials, add a digit (`KN2`). Initials become the suffix of everything you create, so they must be unique within your team.

Every prompt and SQL block in this guide then shows **your** names, ready to copy.
"""
)
require_context()

st.markdown("##### Your names")
st.table(
    [
        {"What": "Role", "Name": f"`{c['role']}`"},
        {"What": "Warehouse", "Name": f"`{c['warehouse']}`"},
        {"What": "Database", "Name": f"`{c['database']}`"},
        {"What": "Schema", "Name": "`CONSUMER`"},
        {"What": "External volume (S3)", "Name": f"`{c['ext_vol']}`"},
        {"What": "Your Iceberg table (exercise 1)", "Name": f"`{c['prices']}`"},
    ],
    hide_index=True,
)
st.caption("The full list for all 15 teams is in **Team names** under Reference.")

st.markdown("#### 2. Sign in and open a SQL file")
st.markdown(
    f"""
1. Open the **Snowsight link** your facilitator posts in the meeting chat and sign in with **your own** TMX login. Never share a login.
2. Open the user menu (your name or initials, bottom left) and switch your role to **`{c['role']}`**.
3. Select **Workspaces** in the left navigation menu, open **My Workspace** and choose **+ Add new → SQL file**. Files here are private to you.
4. Open the **Cortex Code (CoCo) side panel** beside the file. Keep the default model (Auto) and leave tool approvals **on**.
"""
)

st.markdown("#### 3. Set your context")
st.markdown(
    "Paste this into the SQL file and run it (**Run all**, or select it and press Ctrl/Cmd+Enter). It points everything you do next at your team's warehouse, database and schema."
)
st.code(
    f"""USE ROLE {c['role']};
USE WAREHOUSE {c['warehouse']};
USE DATABASE {c['database']};
USE SCHEMA CONSUMER;

SELECT CURRENT_ROLE(), CURRENT_WAREHOUSE(), CURRENT_DATABASE(), CURRENT_SCHEMA();""",
    language="sql",
)
st.markdown(
    f"Also set the same role and warehouse in the **context selector above the editor**, so CoCo's queries run there too. The last line should return `{c['role']}`, `{c['warehouse']}`, `{c['database']}` and `CONSUMER`."
)

render_prompt(
    "0.1",
    "Confirm your context with CoCo",
    f"""What are my current role, warehouse, database and schema? Then check that I can use the external volume {c['ext_vol']} (DESCRIBE EXTERNAL VOLUME) and that I can read {SOURCE_VIEW}. Read-only: do not create, alter or drop anything.""",
)

render_check(
    f"""
- Role **`{c['role']}`**, warehouse **`{c['warehouse']}`**, database **`{c['database']}`**, schema **`CONSUMER`**.
- `DESCRIBE EXTERNAL VOLUME` returns the volume's S3 storage location: it exists and your role can use it.
- CoCo can read the Marketplace view.

If any of these fail, see **Nothing works, or CoCo can't see my objects** below.
"""
)

st.markdown("#### 4. Smoke test")

render_prompt(
    "0.2",
    "Can CoCo see the Marketplace data?",
    f"""Describe the view {SOURCE_VIEW}: its columns and data types, its grain, and the distinct values of VARIABLE. Count its tickers and its earliest and latest DATE for rows from 2026-01-01 onward. Read-only. Cite the fully qualified name you used.""",
)

st.markdown(
    "CoCo shows the SQL it wants to run and waits. **Read it, then approve.** It should be `SELECT`, `SHOW` or `DESCRIBE` only."
)

render_check(
    """
- **Long format**: one row per ticker, date and variable.
- **9 columns**, including `EVENT_TIMESTAMP_UTC` of type **`TIMESTAMP_NTZ(9)`**: remember this one for exercise 1.
- **9 variables**: open, high, low and close (each raw and adjusted), plus `nasdaq_volume`.
- From 2026-01-01: about **13,900 tickers** (every US listing in the source: stocks, ETFs and funds), first date **2026-01-02**. The latest date is about **three months before today**: the free data lags.

Takes about 1 minute.
"""
)

render_learn(
    "Nothing works, or CoCo can't see my objects",
    f"""
- **Role:** the user menu, the SQL file's context selector and the top of the CoCo panel must all show `{c['role']}`. If you can't switch to it, raise your hand: the facilitator checks your Okta group.
- **Warehouse:** `{c['warehouse']}`. If `USE WAREHOUSE` fails, your role hasn't been granted it.
- **Team:** check the sidebar shows the team you were assigned. The names change with it.
- **Marketplace view not found:** the share is mounted as `SNOWFLAKE_CURATED_DATA_FREE`. If it's missing, tell the facilitator.

See **Troubleshooting** in the sidebar for more.
""",
)

st.space("small")
st.page_link("app_pages/ex1_iceberg.py", label="Next: create your Iceberg table", icon=":material/arrow_forward:")
