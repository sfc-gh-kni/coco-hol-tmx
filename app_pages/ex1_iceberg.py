import streamlit as st

from components import (
    SOURCE_VIEW,
    ctx,
    render_check,
    render_go_further,
    render_header,
    render_key_concepts,
    render_learn,
    render_prompt,
    render_review,
    render_takeaways,
    render_tools,
    require_context,
)

c = ctx()

render_header(1, "Create your Iceberg table", "0:20–0:30 (10 min)", "Your own Apache Iceberg table of 2026 US stock prices, stored in your team's S3 volume.")
require_context()

render_tools(
    [
        {"name": "Apache Iceberg table", "icon": "ac_unit", "description": "An open table format: data in Parquet files plus Iceberg metadata, readable by Snowflake and other engines such as Spark."},
        {"name": "External volume", "icon": "cloud", "description": f"A Snowflake object pointing at your team's S3 bucket. `{c['ext_vol']}` is where your table's files are written."},
        {"name": "Snowflake as catalog", "icon": "account_tree", "description": "`CATALOG = 'SNOWFLAKE'` makes the table Snowflake-managed: full SQL reads and writes, and Snowflake maintains the Iceberg metadata."},
    ]
)

st.markdown(
    f"""
The Marketplace view has every US listing back to May 2018, about 170 million rows. You'll copy just 2026 into a table **you** own:

- **Source:** `{SOURCE_VIEW}`
- **Rows:** every ticker, dates from **2026-01-01** onward
- **Target:** `{c['prices']}`, an Iceberg table on `{c['ext_vol']}`

Every later exercise and your app read **this table**, not the Marketplace view.
"""
)

render_prompt(
    "1.1",
    "Create the Iceberg table",
    f"""Create a Snowflake-managed Apache Iceberg table named {c['prices']} with CREATE ICEBERG TABLE ... AS SELECT, using CATALOG = 'SNOWFLAKE' and EXTERNAL_VOLUME = '{c['ext_vol']}'. Select all columns of {SOURCE_VIEW}, but cast EVENT_TIMESTAMP_UTC to TIMESTAMP_NTZ(6), because Iceberg tables only support microsecond precision. Keep only rows with DATE >= '2026-01-01', for every ticker. Use plain CREATE ICEBERG TABLE, not CREATE OR REPLACE, so an existing table is never overwritten. Use warehouse {c['warehouse']}. Show me the statement before running it, and do not create, alter or drop anything else. Afterwards, report the row count, the number of distinct tickers, and the min and max DATE.""",
)

render_review(
    [
        f"It's **`CREATE ICEBERG TABLE {c['prices']}`**: your database, `CONSUMER`, and **your** initials. Not `CREATE OR REPLACE`.",
        f"`CATALOG = 'SNOWFLAKE'` and `EXTERNAL_VOLUME = '{c['ext_vol']}'` come **before** `AS SELECT`.",
        "`EVENT_TIMESTAMP_UTC` is cast with `::TIMESTAMP_NTZ(6)`.",
        "The `WHERE` clause is `DATE >= '2026-01-01'`. Without it you'd copy the whole history back to 2018: about 170 million rows instead of 15 million.",
    ]
)

render_check(
    f"""
Takes about **10–30 seconds** to run (11 seconds on an X-Small warehouse in testing).

| Check | Expected |
| --- | --- |
| Distinct tickers | About **13,900**: every US listing that traded in 2026, stocks and ETFs. **2026-08-13** gave 13,924. |
| Min date | **2026-01-02** (the first trading day of 2026) |
| Max date | The same latest date as the Marketplace view: about three months before today |
| Rows | About **15 million**, and growing by about 100,000 per trading day of new source data. **2026-08-13** gave 15,275,371 (about 140 MB of Parquet in S3). |

**Error `Invalid time type scale ... EVENT_TIMESTAMP_UTC ... TIMESTAMP_NTZ(9)`**: the statement is missing the cast. Ask CoCo to add `::TIMESTAMP_NTZ(6)` and run it again.

**Error `Object '{c['prices']}' already exists`**: you, or a teammate with the same initials, already created it. Run `SHOW ICEBERG TABLES LIKE '{c['table']}' IN SCHEMA {c['schema']};` and check the owner and creation time. If it's yours from an earlier attempt, carry on with it. If it's a teammate's, add a digit to your initials in the sidebar and run 1.1 again.
"""
)

with st.expander(":material/code: Reference SQL, if you'd rather run it yourself"):
    st.code(
        f"""CREATE ICEBERG TABLE {c['prices']}
  CATALOG = 'SNOWFLAKE'
  EXTERNAL_VOLUME = '{c['ext_vol']}'
AS
SELECT ticker, asset_class, primary_exchange_code, primary_exchange_name,
       variable, variable_name, date, value,
       event_timestamp_utc::TIMESTAMP_NTZ(6) AS event_timestamp_utc
FROM {SOURCE_VIEW}
WHERE date >= '2026-01-01';""",
        language="sql",
        wrap_lines=True,
    )

render_prompt(
    "1.2",
    "Prove the copy is complete",
    f"""Verify my new table {c['prices']}. Show its Iceberg properties with SHOW ICEBERG TABLES (catalog, external volume, base location) and its column types. Then compare it with {SOURCE_VIEW} filtered the same way (DATE >= '2026-01-01'): row count, distinct tickers and max DATE must match. Also count the rows and trading days from 2026-01-02 to 2026-06-30 in my table. Read-only.""",
)

render_check(
    f"""
| Check | Expected |
| --- | --- |
| Catalog | `SNOWFLAKE` |
| External volume | `{c['ext_vol']}` |
| Base location | `{c['database']}/CONSUMER/{c['table']}.<random suffix>/`. Snowflake chooses it, because the statement didn't set `BASE_LOCATION`, and the suffix keeps a re-created table from reusing old files |
| Table type | `MANAGED` (Snowflake is the catalog) |
| `EVENT_TIMESTAMP_UTC` type | `TIMESTAMP_NTZ(6)`; the text columns show as `VARCHAR(134217728)`, Iceberg's unbounded string |
| Rows, tickers, max date vs the view | **Identical** |
| 2026-01-02 to 2026-06-30 | **12,124,710 rows**, **123 trading days**, **13,534 tickers** |

The first-half numbers are fixed: that's the window the rest of the lab uses, so everyone's answers match whatever day you run it.
"""
)

render_learn(
    "What this prompt does, and why it's worded this way",
    f"""
| Part of the prompt | Why it's there |
| --- | --- |
| *Snowflake-managed … `CATALOG = 'SNOWFLAKE'`* | Snowflake owns the Iceberg metadata, so you get normal SQL: `SELECT`, `INSERT`, `UPDATE`, views, apps. |
| *`EXTERNAL_VOLUME = '{c['ext_vol']}'`* | The Parquet data and Iceberg metadata files land in **your team's S3 bucket**, where other engines could read them. |
| *Cast to `TIMESTAMP_NTZ(6)`* | The view stores nanoseconds (scale 9). The Iceberg spec stores microseconds, so Snowflake rejects scale 9 rather than silently truncating. |
| *`DATE >= '2026-01-01'`* | The view goes back to 2018 with about 170 million rows. One year keeps your copy to about 15 million rows and 140 MB, so it builds in seconds. |
| *Not `CREATE OR REPLACE`* | Your teammates share this schema. A plain `CREATE` fails rather than overwriting a table that has the same name. |
| *Show the statement first* | It's the only step in the lab that writes data. Read it before you approve it. |

CTAS (`CREATE … AS SELECT`) derives the columns from the query, so you don't type a column list. The storage clauses go **before** `AS SELECT`.
""",
)

render_go_further()

render_prompt(
    "1.3",
    "Where are the files?",
    f"""Run SELECT SYSTEM$GET_ICEBERG_TABLE_INFORMATION('{c['prices']}') and explain the result: where the current metadata file is stored, and how it relates to the external volume {c['ext_vol']}. Then explain in three sentences how another engine, such as Spark, could read this table. Read-only.""",
    optional=True,
)

render_check(
    f"""
The function returns JSON with `"status":"success"` and a `metadataLocation` like `s3://<your team's bucket path>/{c['database']}/CONSUMER/{c['table']}.<suffix>/metadata/00001-<id>.metadata.json`. That's a file in your team's bucket, under the volume's storage location, in the base-location folder from 1.2.

Another engine reads the table through an **Iceberg REST catalog** (Snowflake's Horizon catalog) or straight from that metadata file. It sees the same Parquet files Snowflake wrote: there's one copy of the data, not an export.
"""
)

render_key_concepts(
    [
        ("Apache Iceberg", "An open table format. A table is a set of Parquet data files plus metadata files describing the schema, snapshots and which files make up the current version."),
        ("External volume", "A named, account-level Snowflake object holding the cloud storage location and access identity (here an S3 bucket and IAM role). Tables reference it instead of embedding credentials."),
        ("Snowflake-managed vs externally managed", "With `CATALOG = 'SNOWFLAKE'`, Snowflake writes and maintains the table. With an external catalog (Glue, Polaris), another system owns the metadata and Snowflake mostly reads."),
        ("CTAS", "`CREATE TABLE … AS SELECT`: creates a table and fills it from a query in one statement."),
        ("Initials suffix", f"Everyone on {c['team']} writes to the same `CONSUMER` schema, so `_{c['initials']}` keeps your objects apart from your teammates'."),
    ]
)

render_takeaways(
    [
        "Turned a Marketplace view into your own open-format Iceberg table with one reviewed statement.",
        "Scoped the copy to 2026, so the table is small and fast while still covering every US listing.",
        "Proved the copy matches its source before building on it.",
    ]
)

st.space("small")
st.page_link("app_pages/ex2_discover.py", label="Next: discover the data", icon=":material/arrow_forward:")
