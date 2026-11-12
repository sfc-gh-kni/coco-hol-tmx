import streamlit as st

from components import EXCHANGE_OPERATORS, SOURCE_VIEW, SP500_AS_OF, SP500_TICKERS, ctx

c = ctx()

st.title("Data dictionary")
st.markdown(
    f"""
You build one table in exercise 1, **`{c['prices']}`**. It's an Apache Iceberg copy of the Marketplace view `{SOURCE_VIEW}`, limited to **2026** and the **{len(SP500_TICKERS)} S&P 500 tickers**, and it's stored in your team's external volume `{c['ext_vol']}`.
"""
)

with st.container(horizontal=True):
    st.metric("Tickers", f"{len(SP500_TICKERS)}", border=True)
    st.metric("First date", "2026-01-02", border=True)
    st.metric("Rows, 2026-01-02 → 06-30", "555,048", border=True)
    st.metric("Trading days, first half", "123", border=True)
st.caption("The latest date and total row count depend on when you ran exercise 1: the source adds about 4,500 rows per trading day for these tickers, and lags about three months.")

st.markdown(f"#### `{c['table']}`")
st.markdown("**Grain:** one row per **ticker × date × variable** (long format). 500 of the 503 tickers have all 9 variables on all 123 first-half trading days; BNY, MRSH and ECHO are short (see Traps).")
st.table(
    [
        {"Column": "TICKER", "Type": "VARCHAR", "Description": "Symbol of the US listing, such as `NDAQ` or `BRK.B`"},
        {"Column": "ASSET_CLASS", "Type": "VARCHAR", "Description": "Mostly `Equity` (473) or `REIT` (26)"},
        {"Column": "PRIMARY_EXCHANGE_CODE", "Type": "VARCHAR", "Description": "Primary listing venue: `NYS`, `NAS` or `BAT` (Cboe BZX)"},
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
        {"Group": "Two share classes", "Tickers": "GOOG / GOOGL, FOX / FOXA, NWS / NWSA", "Note": "Why there are 503 tickers for 500 companies"},
        {"Group": "Ticker changed in 2026", "Tickers": "BNY (from BK, 2026-05-21), MRSH (from MMC, 2026-01-14), ECHO (from SATS, 2026-06-24)", "Note": "Short or mixed history under the new ticker"},
    ],
    hide_index=True,
)

with st.expander(f":material/list: All {len(SP500_TICKERS)} tickers"):
    st.markdown(", ".join(f"`{t}`" for t in SP500_TICKERS))
    st.caption(
        f"From the Fidelity 500 Index Fund's SEC N-PORT holdings on {SP500_AS_OF} (Snowflake Curated Data (Free)), mapped to the price data's tickers. "
        "It's a close proxy for index membership on that date, not an official S&P Dow Jones Indices file."
    )

st.markdown("#### Traps to avoid")
st.table(
    [
        {"Trap": "Aggregating without filtering `VARIABLE`", "Symptom": "Averages mix prices and share counts; row counts are 9× too high", "Fix": "Filter to one variable, or pivot first"},
        {"Trap": "Returns on raw close", "Symptom": "Dividend payers look worse than they did", "Fix": "Use `post-market_close_adjusted`"},
        {"Trap": "Ranking tickers with gaps", "Symptom": "BNY tops the list at +1,369%: a different, $10 security used the ticker before BNY Mellon", "Fix": "Keep only tickers with every trading day in the window"},
        {"Trap": "`LAG` on the first day", "Symptom": "2026-01-02 has a `NULL` previous close, and `NULL` sorts first descending", "Fix": "Filter `prev_close IS NOT NULL`, or `DESC NULLS LAST`"},
        {"Trap": "Calling `nasdaq_volume` total volume", "Symptom": "NYSE-listed names look thinly traded", "Fix": "Compare volume over time for one ticker, not across tickers"},
        {"Trap": "Assuming latest means today", "Symptom": "*YTD* silently ends months ago", "Fix": "Use fixed windows, and always show the as-of date"},
        {"Trap": "Treating it as TSX data or the official index", "Symptom": "USD prices; equal-weight averages", "Fix": "Say *US listings* and *equal-weight* in every output"},
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
