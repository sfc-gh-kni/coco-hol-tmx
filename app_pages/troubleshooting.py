import streamlit as st

from components import ctx

c = ctx()

st.title("Troubleshooting")
st.markdown("Find your symptom below. If none fits, post it in the meeting chat with a screenshot. Don't include passwords or personal data.")

ISSUES = [
    (
        "I can't switch to my team role",
        f"""
- Check the sidebar shows **the team you were assigned**: the role name changes with it.
- Your role is **`{c['role']}`**. If it isn't in the user menu's role list, your Okta group hasn't synced. Tell the facilitator.
- If the facilitator says to use the functional role, use `{c['fr_role']}` instead.
""",
    ),
    (
        "CoCo isn't available, or can't see my objects",
        f"""
- Check your role is **`{c['role']}`**: in the user menu, in the SQL file's context selector, and at the top of the CoCo panel.
- Check the warehouse is **`{c['warehouse']}`**.
- Use fully qualified names, for example `{c['prices']}`.
- Still stuck? Ask the facilitator to check your role grants and CoCo access.
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
        "Exercise 1: `Invalid time type scale … TIMESTAMP_NTZ(9)`",
        "The statement copies `EVENT_TIMESTAMP_UTC` without a cast. Iceberg only stores microseconds. Ask CoCo: *Cast EVENT_TIMESTAMP_UTC to TIMESTAMP_NTZ(6) and run it again.*",
    ),
    (
        "Exercise 1: `Object … already exists`",
        f"""
A table with your name is already there.
- Run `SHOW ICEBERG TABLES LIKE '{c['table']}' IN SCHEMA {c['schema']};` and check `created_on`.
- If it's **yours** from an earlier attempt, use it: run prompt 1.2 to confirm it's complete.
- If it's a **teammate's** (same initials), add a digit to your initials in the sidebar, for example `{c['initials']}2`, and run prompt 1.1 again.
- Never `DROP` or `CREATE OR REPLACE` a table you didn't create.
""",
    ),
    (
        "Exercise 1: external volume errors",
        f"""
- **`External volume … does not exist or not authorized`**: check the name is exactly `{c['ext_vol']}`. It starts with `DEV_HACKATHONTOR_`, **without** `EDX`. If it's right, your role lacks `USAGE` on it: tell the facilitator.
- **`Access Denied`** or **`403`** from S3: the volume's IAM setup isn't working for your team. That's an admin fix; tell the facilitator.
- **`Insufficient privileges to operate on schema 'CONSUMER'`**: your role lacks `CREATE ICEBERG TABLE` on the schema. Tell the facilitator.
""",
    ),
    (
        "Exercise 1: CoCo copied far too many rows",
        "If the row count is in the millions, the ticker list was dropped from the `WHERE` clause. Ask a teammate or the facilitator before deleting anything: since the table is yours, you can `DROP ICEBERG TABLE` it and run prompt 1.1 again.",
    ),
    (
        "My numbers don't match the expected answers",
        """
Ask CoCo to show its SQL and check for these common causes:
- **Raw instead of adjusted close.** Returns in exercises 4–6 use `post-market_close_adjusted`.
- **Wrong date window.** Exercise 3 is 2026-04-01 to 2026-06-30. Returns, drawdowns and correlations use 2026-01-02 to 2026-06-30.
- **Tickers with gaps.** Rankings and medians use only tickers with all 123 first-half trading days (excludes BNY, MRSH, ECHO).
- **`NULL` first-day moves.** Filter out rows where the previous close is `NULL`.
- **Long-format mix-up.** The query must filter on `VARIABLE` or pivot first.
- **Rounding.** Small differences in the last decimal place are fine.

A good follow-up prompt: *"Explain why your result differs from X and show the query you used."*
""",
    ),
    (
        "Create Streamlit: preview won't start",
        f"""
- Select the query warehouse **`{c['warehouse']}`** in the dialog. It isn't preselected.
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
Open **Settings → Targets**, set the app location to `{c['schema']}`, the owner role to `{c['role']}` and the warehouse to `{c['warehouse']}`, then click **Save settings**. Deploy unlocks after the settings are saved.
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
        "Click **Cancel questions** and paste prompt 6.1, which tells CoCo not to ask.",
    ),
    (
        "I fell behind",
        "Don't skip exercise 1: everything else reads your Iceberg table. Skip exercise 4 if you need to, and at **1:05** start exercise 5: the app is the main outcome.",
    ),
]

for title, body in ISSUES:
    with st.expander(f":material/help: {title}"):
        st.markdown(body)
