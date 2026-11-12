from pathlib import Path

import streamlit as st

from components import (
    ctx,
    render_check,
    render_checkpoint,
    render_header,
    render_key_concepts,
    render_learn,
    render_prompt,
    render_review,
    render_takeaways,
    render_tools,
    require_context,
)

REFERENCE_APP = Path(__file__).parent.parent / "reference" / "price_explorer.py"

c = ctx()
P = c["prices"]

render_header(5, "Build and deploy an app", "1:05–1:30 (25 min)", "A deployed Streamlit app over your Iceberg table, with numbers you've checked.")
require_context()

st.success(
    "This is the main outcome of the lab. A preview doesn't count: finish with a **deployed** app, opened from outside Workspaces.",
    icon=":material/flag:",
)

render_tools(
    [
        {"name": "Streamlit in Snowflake", "icon": "web", "description": "Python data apps that run inside Snowflake and query governed data directly. No servers, keys or data copies."},
        {"name": "Container runtime", "icon": "deployed_code", "description": "Your app's Python runs on a compute pool (`SYSTEM_COMPUTE_POOL_CPU` by default). Its SQL runs on the query warehouse."},
        {"name": "Deploy target", "icon": "cloud_upload", "description": f"Where the deployed app lives (`{c['schema']}`), which role owns it, and which warehouse and pool it uses."},
    ]
)

st.markdown("##### :material/account_tree: Preview vs deployed")
st.table(
    [
        {"": "Where the code lives", "Preview (Run)": "Your private My Workspace files", "Deployed app": f"A `STREAMLIT` object in `{c['schema']}`"},
        {"": "Who can open it", "Preview (Run)": "Only you, inside Workspaces", "Deployed app": f"Your teammates (role `{c['role']}`), from its link or in Catalog"},
        {"": "Role used for queries", "Preview (Run)": f"`{c['role']}`", "Deployed app": f"The owner role, `{c['role']}`"},
        {"": "When it changes", "Preview (Run)": "Every time you click Run", "Deployed app": "Only when you deploy again"},
    ],
    hide_index=True,
)

render_checkpoint(
    "5.1",
    "Create the app",
    f"""
1. In **My Workspace**, choose **+ Add new → Streamlit app**. Keep it **private**.
2. The **Create Streamlit** dialog says the preview runs with role `{c['role']}`. Fill in:
   - **Title:** `{c['initials']} price explorer`.
   - **Compute pool:** keep the default (`SYSTEM_COMPUTE_POOL_CPU` unless the facilitator says otherwise).
   - **Query warehouse:** select **`{c['warehouse']}`**. It is **not** preselected.
3. Wait for the starter app to preview. The first start takes **30–60 seconds**.
""",
)

render_prompt(
    "5.2",
    "Build the price explorer",
    f"""Build a read-only Streamlit in Snowflake app over my Iceberg table {P}. The sidebar has a searchable ticker multiselect whose options are the distinct tickers in that table, defaulting to NDAQ, ICE, CME and CBOE, with at most 10 selections, and a date range bounded by the table's min and max DATE. Show one metric card per selected ticker (last adjusted close and % return over the range), a line chart of post-market_close_adjusted indexed to 100 at the start of the range, and a bar chart of daily nasdaq_volume. Add a caption with the latest available date and the note that volume is Nasdaq-venue only. Use st.connection("snowflake"), build every number from queries, and only use packages that ship with Streamlit. Do not add packages, external calls, secrets or writes. Edit this app's files and tell me what changed. Do not deploy yet.""",
)

st.markdown(
    """
Open the CoCo side panel **beside the app file** before you paste. Then:

1. CoCo may first show a **plan** and ask *Proceed, modify, or cancel?* Read it and reply **`Proceed`**.
2. When CoCo finishes, review the change and click **Keep**.
3. Click **Run** to refresh the preview.

Building takes about **3 minutes**. Log lines saying `use_container_width` is deprecated are harmless warnings.
"""
)

render_review(
    [
        f"**The plan** names your table, `{P}`, and lists the widgets and charts you asked for. Nothing extra, and no deploy step.",
        "**No new packages:** no added `pyproject.toml` dependencies, `requirements.txt` or `pip install`.",
        "**No writes:** no `INSERT`, `CREATE`, `UPDATE` or `DELETE` in the app's SQL.",
        "**No external calls or secrets:** no `requests`, URLs or `st.secrets`.",
        "**Ticker values** in SQL come from the table's own ticker list (an allow-list), never from free text.",
        "**Returns** use `post-market_close_adjusted`, and the volume caption says Nasdaq-venue only.",
    ],
    title="Before you click Keep",
)

render_check(
    """
Keep the four default tickers and set the range to **2026-01-02 to 2026-06-30**. The metric cards should match exercise 4:

| Ticker | Last adjusted close | Return | Index at 2026-06-30 |
| --- | --- | --- | --- |
| CBOE | $240.83 | −2.3% | 97.7 |
| CME | $219.97 | −15.7% | 84.3 |
| NDAQ | $78.43 | −18.3% | 81.7 |
| ICE | $122.39 | −22.8% | 77.2 |

Your layout, colours and labels will differ from your neighbour's. That's expected.
"""
)

render_learn(
    "What CoCo builds: anatomy of the app",
    f"""
Most generated versions follow the same five-part shape:

**1. Connect.** Container-runtime apps get a ready-made connection with no credentials in the code:
```python
conn = st.connection("snowflake")
```

**2. Load and cache.** A small, cached query for the ticker list and date bounds, so widgets don't re-query on every click:
```python
@st.cache_data(ttl=3600)
def load_universe():
    return conn.query("SELECT TICKER, MIN(DATE) AS MIN_D, MAX(DATE) AS MAX_D FROM {P} GROUP BY TICKER")
```

**3. Sidebar filters.** `st.multiselect` over the table's ~13,900 tickers (type to search) and `st.date_input` bounded by `MIN(DATE)` and `MAX(DATE)`.

**4. Query the selection.** A pivot like exercise 3, limited to the selected tickers and dates. Tickers come from the table, an allow-list, never from free text.

**5. Show it.** `st.metric` cards, then a line chart of `100 * close / first close` and a bar chart of volume.

The app doesn't know or care that the table is Iceberg: it's just SQL. If your version differs, that's fine. Check that it still meets the rules in *Before you click Keep*.
""",
)

render_checkpoint(
    "5.3",
    "Deploy and open it",
    f"""
1. Open the app's **Settings → Targets** and set:

   | Setting | Value |
   | --- | --- |
   | App location | `{c['schema']}` |
   | Owner role | `{c['role']}` |
   | Warehouse | `{c['warehouse']}` |
   | Compute pool | Same as the preview (default `SYSTEM_COMPUTE_POOL_CPU`) |
   | App ID | **Leave blank**: Snowsight generates a unique ID |

2. Click **Save settings**. The **Deploy** button stays greyed out until you do.
3. Click **Deploy**. It takes about **30 seconds**.
4. Open the deployed app: in the left navigation menu go to **Catalog → Explorer**, open `{c['database']}` → `CONSUMER` → **Streamlits**, and select your app. The first cold start takes about **45 seconds**.
5. Check that the deployed app shows the **same numbers** as your preview.
6. Copy the app's link and post it in your team's chat.
""",
)

with st.expander(":material/bug_report: Preview shows an error? Paste this into CoCo"):
    st.code(
        """Debug this Streamlit preview error without changing the database, adding network access or installing packages. Explain the cause and show the smallest fix for review.""",
        language="text",
        wrap_lines=True,
    )

st.markdown("##### Finished early? Stretch ideas")
st.markdown(
    """
These aren't part of the checked path. Ask CoCo to:
- add **SPY** as a dashed **benchmark line** on the indexed chart, whatever tickers are selected. For 2026-01-02 to 2026-06-30 it should end at **109.9** (QQQ ends at 120.3, EWC at 106.9);
- add a drawdown chart (percent below the running peak). For the exchange operators it should bottom at the **end of June**, between −23% (NDAQ) and −37% (CBOE), against −9% for SPY, as in prompt 4.2;
- add a **compare to peers** mode: pick one ticker and show its return against SPY, QQQ and EWC over the selected range;
- add a **download** button for the filtered data as CSV.

Review each change before you click **Keep**, and redeploy to publish it.
"""
)

with st.expander(":material/code: Reference solution"):
    st.markdown(
        "A complete version of the app, with `PRICES` set to your table. "
        "Use it to compare approaches, not to replace your own: the outcome is an app you built and reviewed with CoCo."
    )
    code = REFERENCE_APP.read_text().replace(
        'PRICES = "DEV_EDX_HACKATHONTOR_<TEAM>_DB.CONSUMER.STOCK_PRICE_TIMESERIES_<INITIALS>"',
        f'PRICES = "{P}"',
    )
    st.code(code, language="python", line_numbers=True)

render_learn(
    "Who can see and change my app?",
    f"""
Everyone on **{c['team']}** deploys into `{c['schema']}` with the same team role, `{c['role']}`. That makes setup simple, but it also means your teammates can see, and could change, your deployed app and your table. That's why the ground rules ask you to touch only objects ending in `_{c['initials']}` or titled with your initials. Other teams use their own database and role. Your source files in **My Workspace** stay private.

The deployed app runs its queries as the **owner role**, not as the person viewing it.
""",
)

render_key_concepts(
    [
        ("Streamlit in Snowflake", "A Streamlit app stored and run as a Snowflake object. Data never leaves Snowflake, and access is controlled by roles like any other object."),
        ("Compute pool vs warehouse", "The **compute pool** runs the app's Python process. The **query warehouse** runs its SQL. You picked both in the Create Streamlit dialog and the deploy target."),
        ("Owner role", "The role that owns the deployed app. Its privileges decide what the app's queries can read, whoever is viewing."),
        ("`st.cache_data`", "Caches a function's result so repeat interactions don't re-run the same query. It makes apps faster and cheaper."),
        ("Plan checkpoint", "For multi-step work CoCo proposes a plan and waits. Replying *Proceed*, *modify* or *cancel* keeps you in control before any file changes."),
    ]
)

render_takeaways(
    [
        "Turned a written spec into a working app with CoCo, with a review checkpoint before the code changed.",
        "Checked the app's numbers against independently verified answers.",
        f"Deployed it into `{c['schema']}` and opened the live app.",
    ]
)
