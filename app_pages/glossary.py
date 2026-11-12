import streamlit as st

from components import ctx

c = ctx()

st.title("Glossary")
st.markdown("Terms used in this lab, in alphabetical order. Search the page with your browser's find shortcut.")

TERMS = {
    "Snowflake and CoCo": [
        ("Approval", "CoCo's pause before it runs SQL or changes a file. Keep approvals on in this lab."),
        ("CoCo (Cortex Code)", "Snowflake's AI coding agent in Snowsight. It explores data, writes SQL and builds apps and reports, under your role."),
        ("CoCo side panel", "The CoCo chat docked beside an open file in Workspaces. It uses that file as context."),
        ("Compute pool", "Managed container nodes that run Streamlit apps on the container runtime. The default is `SYSTEM_COMPUTE_POOL_CPU`."),
        ("Container runtime", "The way Streamlit in Snowflake runs apps: a Python process on a compute pool, with SQL sent to a warehouse."),
        ("Context", "The current role, warehouse, database and schema for your session, set with `USE` statements or the context selector."),
        ("Deploy target", "Settings for the deployed app: location (database.schema), owner role, warehouse, compute pool and app ID."),
        ("Fully qualified name", f"`DATABASE.SCHEMA.OBJECT`, such as `{c['prices']}`. It removes ambiguity for you and for CoCo."),
        ("Functional role", f"A role that holds privileges, such as `{c['fr_role']}`. It's granted to the Okta role you sign in with."),
        ("HTML report", "A self-contained `.html` file in Workspaces that embeds a snapshot of query results."),
        ("Marketplace", "Snowflake's catalog of shared datasets. Shared data appears as a read-only database, here `SNOWFLAKE_CURATED_DATA_FREE`."),
        ("My Workspace", "Your private file area in Snowsight Workspaces. Other attendees can't see it."),
        ("Okta role", f"The role your TMX sign-in grants you, such as `{c['role']}`. Select it in Snowsight."),
        ("Owner role", "The role that owns an object. For an app, it decides what the app's queries can read."),
        ("Role", "A named set of privileges. Each team has its own."),
        ("Skill", "A packaged set of instructions CoCo loads for a type of task, such as SQL authoring, Streamlit in Workspaces or HTML authoring."),
        ("Snowflake Curated Data", "Free, ready-to-query public datasets from Snowflake, available through the Marketplace."),
        ("Streamlit in Snowflake", "Python data apps stored and run as Snowflake objects, governed by roles."),
        ("View", "A saved query. It stores no data and reads its source tables each time it's queried."),
        ("Warehouse", f"Snowflake compute that runs SQL. Your team uses `{c['warehouse']}`."),
    ],
    "Iceberg": [
        ("Apache Iceberg", "An open table format: Parquet data files plus metadata files that track the schema, snapshots and the files in each version. Readable by many engines."),
        ("Base location", "The folder under the external volume where a table's files go. If you don't set `BASE_LOCATION`, Snowflake uses `<database>/<schema>/<table>.<random suffix>/`."),
        ("Catalog", "The service that tracks where an Iceberg table's current metadata file is. `CATALOG = 'SNOWFLAKE'` makes Snowflake the catalog."),
        ("CTAS", "`CREATE TABLE … AS SELECT`: creates a table and fills it from a query in one statement."),
        ("External volume", f"A Snowflake object naming a cloud storage location and the identity used to access it. Your team's is `{c['ext_vol']}`, an S3 bucket."),
        ("Metadata file", "A JSON file (`….metadata.json`) describing an Iceberg table's current state. Each change writes a new one."),
        ("Parquet", "The columnar file format Iceberg uses for data."),
        ("Snowflake-managed Iceberg table", "An Iceberg table with Snowflake as catalog: full read and write SQL, and Snowflake maintains the files."),
        ("Timestamp precision", "Iceberg stores timestamps to the microsecond, so Snowflake Iceberg columns use `TIMESTAMP_NTZ(6)`, not scale 9."),
    ],
    "SQL": [
        ("CTE", "Common table expression: a named intermediate result introduced with `WITH`."),
        ("Conditional aggregation", "`MAX(IFF(condition, value, NULL))` in a `GROUP BY` to turn rows into columns."),
        ("COUNT_IF", "Snowflake function that counts the rows where a condition is true."),
        ("Grain", "What one row represents, such as *ticker × date*."),
        ("LAG", "Window function that returns a value from the previous row in the window, or `NULL` on the first row."),
        ("Long format", "One row per entity, date and measure. The opposite of wide format, with one column per measure."),
        ("MIN_BY / MAX_BY", "Return the value of one column at the row where another column is smallest or largest."),
        ("NULLS FIRST / LAST", "Where `NULL` goes in a sort. Snowflake's default is last ascending and first descending."),
        ("PIVOT", "Snowflake syntax that turns distinct row values into columns."),
        ("QUALIFY", "Filters rows on the result of a window function."),
        ("RANK", "Window function that numbers rows by a sort order, giving ties the same rank."),
        ("Window function", "A calculation over a set of related rows that keeps every row (`OVER (PARTITION BY … ORDER BY …)`)."),
    ],
    "Markets": [
        ("Adjusted price", "A price rescaled for dividends and splits, so returns over time are comparable."),
        ("Consolidated volume", "Total shares traded across all venues. `nasdaq_volume` is only the Nasdaq slice of it."),
        ("Correlation", "From −1 to +1: how closely two return series move together."),
        ("Drawdown", "Percent fall from the running peak. Maximum drawdown is the worst such fall in a period."),
        ("Equal-weight average", "The average of every stock's daily return, each counted equally. The official S&P 500 is weighted by company size instead."),
        ("Exchange operator", "A company that runs trading venues and clearing, such as Nasdaq, ICE, CME and Cboe."),
        ("Indexed to 100", "Each series divided by its first value and multiplied by 100, so different price levels share one chart."),
        ("S&P 500", "An index of about 500 large US companies. The lab uses an index fund's holdings list as the membership."),
        ("Ticker change", "A company moving to a new symbol, such as MMC → MRSH. Price data keyed by ticker splits the history at the change."),
    ],
}

for section, terms in TERMS.items():
    st.markdown(f"#### {section}")
    st.table([{"Term": t, "Meaning": d} for t, d in terms], hide_index=True)
