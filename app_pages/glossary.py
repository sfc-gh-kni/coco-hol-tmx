import streamlit as st

st.title("Glossary")
st.markdown("Terms used in this lab, in alphabetical order. Search the page with your browser's find shortcut.")

TERMS = {
    "Snowflake and CoCo": [
        ("Approval", "CoCo's pause before it runs SQL or changes a file. Keep approvals on in this lab."),
        ("CoCo (Cortex Code)", "Snowflake's AI coding agent in Snowsight. It explores data, writes SQL and builds apps and reports, under your role."),
        ("CoCo side panel", "The CoCo chat docked beside an open file in Workspaces. It uses that file as context."),
        ("Compute pool", "Managed container nodes that run Streamlit apps on the container runtime. The lab uses `SYSTEM_COMPUTE_POOL_CPU`."),
        ("Container runtime", "The way Streamlit in Snowflake runs apps: a Python process on a compute pool, with SQL sent to a warehouse."),
        ("Deploy target", "Settings for the deployed app: location (database.schema), owner role, warehouse, compute pool and app ID."),
        ("Fully qualified name", "`DATABASE.SCHEMA.OBJECT`, such as `TMX_COCO_HOL.SOURCE.WATCHLIST`. It removes ambiguity for you and for CoCo."),
        ("HTML report", "A self-contained `.html` file in Workspaces that embeds a snapshot of query results."),
        ("My Workspace", "Your private file area in Snowsight Workspaces. Other attendees can't see it."),
        ("Owner role", "The role that owns an object. For an app, it decides what the app's queries can read."),
        ("Role", "A named set of privileges. Everyone in this lab uses `TMX_HOL_ATTENDEE`."),
        ("Skill", "A packaged set of instructions CoCo loads for a type of task, such as SQL authoring, Streamlit in Workspaces or HTML authoring."),
        ("Snowflake Curated Data", "Free, ready-to-query public datasets from Snowflake, available through the Marketplace."),
        ("Streamlit in Snowflake", "Python data apps stored and run as Snowflake objects, governed by roles."),
        ("Warehouse", "Snowflake compute that runs SQL. The lab uses `TMX_HOL_WH`."),
    ],
    "SQL": [
        ("CTE", "Common table expression: a named intermediate result introduced with `WITH`."),
        ("Conditional aggregation", "`MAX(IFF(condition, value, NULL))` in a `GROUP BY` to turn rows into columns."),
        ("COUNT_IF", "Snowflake function that counts the rows where a condition is true."),
        ("Grain", "What one row represents, such as *ticker × date*."),
        ("LAG", "Window function that returns a value from the previous row in the window."),
        ("Long format", "One row per entity, date and measure. The opposite of wide format, with one column per measure."),
        ("MIN_BY / MAX_BY", "Return the value of one column at the row where another column is smallest or largest."),
        ("PIVOT", "Snowflake syntax that turns distinct row values into columns."),
        ("QUALIFY", "Filters rows on the result of a window function."),
        ("Window function", "A calculation over a set of related rows that keeps every row (`OVER (PARTITION BY … ORDER BY …)`)."),
    ],
    "Markets": [
        ("Adjusted price", "A price rescaled for dividends and splits, so returns over time are comparable."),
        ("Benchmark ETF", "A fund tracking an index, used for comparison: SPY (S&P 500), QQQ (Nasdaq-100), EWC (MSCI Canada)."),
        ("Consolidated volume", "Total shares traded across all venues. `nasdaq_volume` is only the Nasdaq slice of it."),
        ("Correlation", "From −1 to +1: how closely two return series move together."),
        ("Drawdown", "Percent fall from the running peak. Maximum drawdown is the worst such fall in a period."),
        ("Exchange operator", "A company that runs trading venues and clearing, such as Nasdaq, ICE, CME and Cboe."),
        ("Indexed to 100", "Each series divided by its first value and multiplied by 100, so different price levels share one chart."),
        ("Interlisted", "Listed on more than one exchange, such as RY on both TSX and NYSE. This lab only has the US listing."),
        ("YTD", "Year to date: from the first trading day of the year to the latest available date."),
    ],
}

for section, terms in TERMS.items():
    st.markdown(f"#### {section}")
    st.table([{"Term": t, "Meaning": d} for t, d in terms], hide_index=True)
