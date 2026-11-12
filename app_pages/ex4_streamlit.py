import streamlit as st

from components import (
    APP_SCHEMA,
    ROLE,
    WAREHOUSE,
    render_check,
    render_checkpoint,
    render_header,
    render_learn,
    render_prompt,
    render_takeaways,
)

render_header(4, "Build and deploy an app", "1:05–1:30 (25 min)", "A deployed Streamlit app of your own, with numbers you've checked.")

st.success(
    "This is the main outcome of the lab. A preview doesn't count: finish with a **deployed** app you can open from **Projects → Streamlit**.",
    icon=":material/flag:",
)

render_checkpoint(
    "4.1",
    "Create the app",
    f"""
1. In **My Workspace**, choose **+ Add new → Streamlit app**. Keep it **private**.
2. The **Create Streamlit** dialog says the preview runs with role `{ROLE}`. Fill in:
   - **Title:** your initials plus `price explorer`, for example `KN price explorer`.
   - **Compute pool:** keep the default (`SYSTEM_COMPUTE_POOL_CPU` unless the facilitator says otherwise).
   - **Query warehouse:** select **`{WAREHOUSE}`**. It is **not** preselected.
3. Wait for the starter app to preview. The first start takes **30–60 seconds**.
""",
)

render_prompt(
    "4.2",
    "Build the price explorer",
    """Build a read-only Streamlit in Snowflake app over TMX_COCO_HOL.SOURCE.STOCK_PRICE_TIMESERIES and TMX_COCO_HOL.SOURCE.WATCHLIST. The sidebar has a segment filter, a ticker multiselect limited to the watchlist, and a date range bounded by the data's min and max dates. Show one metric card per selected ticker (last adjusted close and % return over the range), a line chart of adjusted close indexed to 100 at the start of the range, and a bar chart of daily nasdaq_volume. Add a caption with the latest available date and the note that volume is Nasdaq-venue only. Use st.connection("snowflake"), build every number from queries, and only use packages that ship with Streamlit. Do not add packages, external calls, secrets or writes. Edit this app's files and tell me what changed. Do not deploy yet.""",
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

render_check(
    """
Choose the **Exchange operator** segment and the range **2026-01-02 to 2026-08-12**. The metric cards should show the same returns as exercise 3:

| Ticker | Return |
| --- | --- |
| CBOE | +18.1% |
| CME | +0.1% |
| NDAQ | −0.6% |
| ICE | −4.9% |

Your layout, colours and labels will differ from your neighbour's. That's expected.
"""
)

render_checkpoint(
    "4.3",
    "Deploy and open it",
    f"""
1. Open the app's **Settings → Targets** and set:

   | Setting | Value |
   | --- | --- |
   | App location | `{APP_SCHEMA}` |
   | Owner role | `{ROLE}` |
   | Warehouse | `{WAREHOUSE}` |
   | Compute pool | Same as the preview (default `SYSTEM_COMPUTE_POOL_CPU`) |
   | App ID | **Leave blank**: Snowsight generates a unique ID |

2. Click **Save settings**. The **Deploy** button stays greyed out until you do.
3. Click **Deploy**. It takes about **30 seconds**.
4. Open your app from **Projects → Streamlit**. The first cold start takes about **45 seconds**.
5. Check that the deployed app shows the **same numbers** as your preview.
6. Copy the app's link and post it in the meeting chat.
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
These aren't part of the checked path, so there are no expected answers. Ask CoCo to:
- add a **drawdown** chart (percent below the running peak) for the selected tickers;
- add a toggle between **adjusted** and **raw** close, with a note on why they differ;
- add a **download** button for the filtered data as CSV.

Review each change before you click **Keep**, and redeploy to publish it.
"""
)

render_learn(
    "Who can see and change my app?",
    f"""
Everyone in the lab deploys into `{APP_SCHEMA}` with the same owner role, `{ROLE}`. That makes setup simple, but it also means other attendees can see and could change your deployed app. That's why the ground rules ask you to touch only your own. Your source files in **My Workspace** stay private.

The deployed app runs its queries as the **owner role**, not as the person viewing it.
""",
)

render_takeaways(
    [
        "Turned a written spec into a working app with CoCo, with a review checkpoint before the code changed.",
        "Checked the app's numbers against independently verified answers.",
        f"Deployed it into `{APP_SCHEMA}` and opened the live app.",
    ]
)
