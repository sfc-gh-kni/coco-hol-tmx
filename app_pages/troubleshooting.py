import streamlit as st

from components import APP_SCHEMA, ROLE, WAREHOUSE

st.title("Troubleshooting")
st.markdown("Find your symptom below. If none fits, post it in the meeting chat with a screenshot. Don't include passwords or personal data.")

ISSUES = [
    (
        "CoCo isn't available, or can't see the tables",
        f"""
- Check your role is **`{ROLE}`**: in the user menu, in the SQL file's context selector, and at the top of the CoCo panel.
- Check the warehouse is **`{WAREHOUSE}`**.
- Use fully qualified names, for example `TMX_COCO_HOL.SOURCE.WATCHLIST`.
- Still stuck? Ask the facilitator to check your role grant and CoCo access.
""",
    ),
    (
        "CoCo is waiting and nothing happens",
        """
CoCo is probably waiting for **you**. Look in the panel for:
- an **approval** prompt for SQL or a tool;
- a **plan** asking *Proceed, modify, or cancel?* (reply `Proceed`);
- a file change waiting for **Keep** or **Undo**.
""",
    ),
    (
        "My numbers don't match the expected answers",
        """
Ask CoCo to show its SQL and check for these common causes:
- **Raw instead of adjusted close.** Returns in exercises 3–5 use `post-market_close_adjusted`.
- **Wrong date window.** Exercise 2 is 2026-04-01 to 2026-06-30. YTD is 2026-01-02 to 2026-08-12.
- **Long-format mix-up.** The query must filter on `VARIABLE` or pivot first.
- **Rounding.** Small differences in the last decimal place are fine.

A good follow-up prompt: *"Explain why your result differs from X and show the query you used."*
""",
    ),
    (
        "Create Streamlit: preview won't start",
        f"""
- Select the query warehouse **`{WAREHOUSE}`** in the dialog. It isn't preselected.
- Wait 30–60 seconds. The first start is a cold start.
- If many people start at once, it can take longer. Wait a minute before retrying.
""",
    ),
    (
        "App preview shows an error",
        """
Paste this into the CoCo panel beside the app file:

```text
Debug this Streamlit preview error without changing the database, adding network access or installing packages. Explain the cause and show the smallest fix for review.
```

Log lines about `use_container_width` being deprecated are only warnings.
""",
    ),
    (
        "The Deploy button is greyed out",
        f"""
Open **Settings → Targets**, set the app location to `{APP_SCHEMA}`, the owner role to `{ROLE}` and the warehouse to `{WAREHOUSE}`, then click **Save settings**. Deploy unlocks after the settings are saved.
""",
    ),
    (
        "Deploy fails with a name or ID conflict",
        "Leave **App ID** blank so Snowsight generates a unique one. Never reuse someone else's app ID.",
    ),
    (
        "My deployed app looks different from my preview",
        "Redeploy after your last **Keep**: the deployed app only changes when you deploy again. Then reload the deployed app.",
    ),
    (
        "The Report option asks me questions",
        "Click **Cancel questions** and paste prompt 5.1, which tells CoCo not to ask.",
    ),
    (
        "I fell behind",
        "Skip exercise 3. At **1:05**, start exercise 4: the app is the main outcome. Come back to exercises 1–3 afterwards if lab access is still open.",
    ),
]

for title, body in ISSUES:
    with st.expander(f":material/help: {title}"):
        st.markdown(body)
