import streamlit as st

from components import BENCHMARK_ETFS, CANADIAN_INTERLISTED, EXCHANGE_OPERATORS, SOURCE_VIEW, ctx

c = ctx()

st.title("Data dictionary")
st.markdown(
    f"""
You build one table in exercise 1, **`{c['prices']}`**. It's an Apache Iceberg copy of the Marketplace view `{SOURCE_VIEW}`, limited to **2026** but with **every ticker**, and it's stored in your team's external volume `{c['ext_vol']}`.
"""
)

with st.container(horizontal=True):
    st.metric("Tickers", "~13,900", border=True)
    st.metric("First date", "2026-01-02", border=True)
    st.metric("Rows, 2026-01-02 → 06-30", "12,124,710", border=True)
    st.metric("Trading days, first half", "123", border=True)
st.caption("The latest date, total rows and ticker count depend on when you ran exercise 1: the source adds about 100,000 rows per trading day, and lags about three months. 2026-08-13 gave 15,275,371 rows and 13,924 tickers.")

st.markdown(f"#### `{c['table']}`")
st.markdown("**Grain:** one row per **ticker × date × variable** (long format). In the first half, 7,534 of the 13,534 tickers have all 9 variables on all 123 trading days; the rest listed, delisted, changed ticker or traded only some days (exercise 2.2).")
st.table(
    [
        {"Column": "TICKER", "Type": "VARCHAR", "Description": "Symbol of the US listing, such as `NDAQ`, `SPY` or `RY`"},
        {"Column": "ASSET_CLASS", "Type": "VARCHAR", "Description": "Mostly `Equity` (7,194 in the first half) or `ETF-Index Fund Shares` (5,473), then closed-end funds, REITs and others"},
        {"Column": "PRIMARY_EXCHANGE_CODE", "Type": "VARCHAR", "Description": "Primary listing venue, such as `NYS` (NYSE), `NAS` (Nasdaq), `PSE` (NYSE Arca) or `BAT` (Cboe BZX)"},
        {"Column": "PRIMARY_EXCHANGE_NAME", "Type": "VARCHAR", "Description": "Full name of the primary listing venue"},
        {"Column": "VARIABLE", "Type": "VARCHAR", "Description": "Machine name of the measure (see below). **Always filter or pivot on this.**"},
        {"Column": "VARIABLE_NAME", "Type": "VARCHAR", "Description": "Human-readable label, such as `Post-Market Close Adjusted`"},
        {"Column": "DATE", "Type": "DATE", "Description": "Trading date, from 2026-01-02"},
        {"Column": "VALUE", "Type": "FLOAT", "Description": "The measure's value: USD for prices, shares for volume"},
        {"Column": "EVENT_TIMESTAMP_UTC", "Type": "TIMESTAMP_NTZ(6)", "Description": "When the source recorded the value. Scale 9 in the view; cast to 6 because Iceberg stores microseconds"},
    ],
    hide_index=True,
)
st.caption("Text columns show as `VARCHAR(134217728)`: Iceberg's `string` type has no length limit.")

st.markdown("##### The 9 variables, with NDAQ on 2026-06-30 as an example")
st.table(
    [
        {"VARIABLE": "pre-market_open", "Meaning": "Opening price", "NDAQ": "77.37"},
        {"VARIABLE": "pre-market_open_adjusted", "Meaning": "Opening price, adjusted for dividends and splits", "NDAQ": "77.11"},
        {"VARIABLE": "all-day_high", "Meaning": "Day's high", "NDAQ": "79.25"},
        {"VARIABLE": "all-day_high_adjusted", "Meaning": "Day's high, adjusted", "NDAQ": "78.98"},
        {"VARIABLE": "all-day_low", "Meaning": "Day's low", "NDAQ": "76.55"},
        {"VARIABLE": "all-day_low_adjusted", "Meaning": "Day's low, adjusted", "NDAQ": "76.29"},
        {"VARIABLE": "post-market_close", "Meaning": "Closing price", "NDAQ": "78.70"},
        {"VARIABLE": "post-market_close_adjusted", "Meaning": "Closing price, adjusted: **use this for returns**", "NDAQ": "78.43"},
        {"VARIABLE": "nasdaq_volume", "Meaning": "Shares traded on **Nasdaq venues only**", "NDAQ": "2,160,991"},
    ],
    hide_index=True,
)

st.markdown("#### Tickers to know")
st.table(
    [
        {"Group": "Exchange operators (the lab's focus)", "Tickers": ", ".join(EXCHANGE_OPERATORS), "Note": "NDAQ and CME list on Nasdaq, ICE on NYSE, CBOE on Cboe BZX"},
        {"Group": "Benchmark ETFs", "Tickers": ", ".join(BENCHMARK_ETFS), "Note": "S&P 500, Nasdaq-100 and MSCI Canada index funds"},
        {"Group": "Canadian interlisted", "Tickers": ", ".join(CANADIAN_INTERLISTED), "Note": "US (NYSE) listings in USD, not the TSX listings"},
        {"Group": "Ticker changed in 2026", "Tickers": "MMC → MRSH (2026-01-14), BK → BNY (2026-05-21), SATS → ECHO (2026-06-24)", "Note": "The history splits across two tickers; `BNY` was used by a different security before"},
    ],
    hide_index=True,
)

st.markdown("#### Traps to avoid")
st.table(
    [
        {"Trap": "Aggregating without filtering `VARIABLE`", "Symptom": "Averages mix prices and share counts; row counts are 9× too high", "Fix": "Filter to one variable, or pivot first"},
        {"Trap": "Returns on raw close", "Symptom": "Dividend payers look worse than they did", "Fix": "Use `post-market_close_adjusted`"},
        {"Trap": "Comparing tickers with gaps", "Symptom": "BNY's close jumps from about $10 to $139 on 2026-05-21: a different security used the ticker before BNY Mellon", "Fix": "Check every ticker has all trading days in the window"},
        {"Trap": "`LAG` on the first day", "Symptom": "2026-01-02 has a `NULL` previous close, and `NULL` sorts first descending", "Fix": "Filter `prev_close IS NOT NULL`, or `DESC NULLS LAST`"},
        {"Trap": "Calling `nasdaq_volume` total volume", "Symptom": "NYSE-listed names look thinly traded", "Fix": "Compare volume over time for one ticker, not across tickers"},
        {"Trap": "Assuming latest means today", "Symptom": "*YTD* silently ends months ago", "Fix": "Use fixed windows, and always show the as-of date"},
        {"Trap": "Reading the whole table in an app", "Symptom": "Slow charts: about 15 million rows", "Fix": "Filter by ticker, variable and date in SQL, not in pandas"},
        {"Trap": "Treating it as TSX data", "Symptom": "RY and TD in USD, at NYSE prices", "Fix": "Say *US listings, USD* in every output"},
    ],
    hide_index=True,
)

st.markdown("#### Starter queries")
st.code(
    f"""-- Shape of your table
SELECT COUNT(*) AS n_rows, COUNT(DISTINCT ticker) AS tickers,
       COUNT(DISTINCT date) AS trading_days, MIN(date), MAX(date)
FROM {c['prices']};

-- Long to wide: one row per ticker and date
SELECT ticker, date,
       MAX(IFF(variable = 'post-market_close_adjusted', value, NULL)) AS adj_close,
       MAX(IFF(variable = 'nasdaq_volume', value, NULL))              AS nasdaq_volume
FROM {c['prices']}
WHERE ticker = 'NDAQ' AND date BETWEEN '2026-06-22' AND '2026-06-30'
GROUP BY ticker, date
ORDER BY date;

-- Iceberg properties
SHOW ICEBERG TABLES LIKE '{c['table']}' IN SCHEMA {c['schema']};""",
    language="sql",
)

st.markdown(
    "Source documentation: [Snowflake Curated Data: stocks](https://data-docs.snowflake.com/sources/stocks) · "
    "[Apache Iceberg tables in Snowflake](https://docs.snowflake.com/en/user-guide/tables-iceberg)."
)
