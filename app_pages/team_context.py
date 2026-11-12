import pandas as pd
import streamlit as st

from components import PREFIX, S3_PREFIX, SCHEMA, TEAMS, ctx, team_names

st.title("Team names")
st.markdown(
    f"""
Every team has its own role, warehouse, database and external volume. Everything starts with `{PREFIX}_`, except the S3 external volume, which starts with `{S3_PREFIX}_`. Each database has a **`{SCHEMA}`** schema, created by the admin, where your Iceberg table, views and app go.
"""
)

c = ctx()
if c["ready"]:
    st.success(f"You've picked **{c['team']}**. Your row is highlighted.", icon=":material/badge:")

rows = []
for i, team in enumerate(TEAMS, start=1):
    names = team_names(team)
    rows.append(
        {
            "#": i,
            "Team": team,
            "Role (use this)": names["Role"],
            "Warehouse": names["Warehouse"],
            "Database": names["Database"],
            "Schema": SCHEMA,
            "External volume": names["External volume"],
        }
    )


def _highlight(row):
    return ["background-color: rgba(41, 181, 232, 0.18)" if row["Team"] == c["team"] else "" for _ in row]


st.dataframe(
    pd.DataFrame(rows).style.apply(_highlight, axis=1),
    hide_index=True,
    height=35 * (len(rows) + 1) + 3,
)

st.markdown("#### Roles")
st.markdown(
    f"""
Each team has two roles:

| Role | What it's for |
| --- | --- |
| `{PREFIX}_<TEAM>_ANALYST_OKTA` | The role you're given through your TMX (Okta) sign-in. **Select this one** in Snowsight. |
| `{PREFIX}_<TEAM>_ANALYST_FR` | The team's functional role. It holds the privileges (warehouse, database, external volume, Marketplace data) and is granted to the Okta role, so you get them automatically. |

If your facilitator tells you to use the `_FR` role directly, do that instead.
"""
)
