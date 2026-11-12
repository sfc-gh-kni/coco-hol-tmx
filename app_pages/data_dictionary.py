import streamlit as st

from components import PRICES, WATCHLIST

st.title("Data dictionary")
st.markdown(
    "Two read-only tables in `TMX_COCO_HOL.SOURCE`. They're a frozen snapshot of the **Snowflake Curated Data (Free)** stock price time series, limited to a 14-ticker watchlist from 2024 onward."
)

with st.container(horizontal=True):
    st.metric("Rows", "82,404", border=True)
    st.metric("Tickers", "14", border=True)
    st.metric("Trading days", "654", border=True)
    st.metric("Date range", "2024-01-02 → 2026-08-12", border=True)

st.markdown(f"#### `{PRICES}`")
st.markdown("**Grain:** one row per **ticker × date × variable** (long format). Every ticker has all 9 variables on all 654 trading days.")
st.table(
    [
        {"Column": "TICKER", "Type": "TEXT", "Description": "Symbol of the US listing, such as `RY` or `NDAQ`"},
        {"Column": "ASSET_CLASS", "Type": "TEXT", "Description": "`Equity`, `ETF-Index Fund Shares` or `ETF-Portfolio Depositary Receipt`"},
        {"Column": "PRIMARY_EXCHANGE_CODE", "Type": "TEXT", "Description": "Primary listing venue: `NYS`, `NAS`, `PSE` (NYSE Arca) or `BAT` (Cboe BZX)"},
        {"Column": "PRIMARY_EXCHANGE_NAME", "Type": "TEXT", "Description": "Full name of the primary listing venue"},
        {"Column": "VARIABLE", "Type": "TEXT", "Description": "Machine name of the measure (see below). **Always filter or pivot on this.**"},
        {"Column": "VARIABLE_NAME", "Type": "TEXT", "Description": "Human-readable label, such as `Post-Market Close Adjusted`"},
        {"Column": "DATE", "Type": "DATE", "Description": "Trading date"},
        {"Column": "VALUE", "Type": "FLOAT", "Description": "The measure's value: USD for prices, shares for volume"},
    ],
    hide_index=True,
)

st.markdown("##### The 9 variables, with RY on 2026-08-12 as an example")
st.table(
    [
        {"VARIABLE": "pre-market_open", "Meaning": "Opening price", "RY": "211.57"},
        {"VARIABLE": "pre-market_open_adjusted", "Meaning": "Opening price, adjusted for dividends and splits", "RY": "210.25"},
        {"VARIABLE": "all-day_high", "Meaning": "Day's high", "RY": "213.69"},
        {"VARIABLE": "all-day_high_adjusted", "Meaning": "Day's high, adjusted", "RY": "212.36"},
        {"VARIABLE": "all-day_low", "Meaning": "Day's low", "RY": "210.42"},
        {"VARIABLE": "all-day_low_adjusted", "Meaning": "Day's low, adjusted", "RY": "209.11"},
        {"VARIABLE": "post-market_close", "Meaning": "Closing price", "RY": "213.69"},
        {"VARIABLE": "post-market_close_adjusted", "Meaning": "Closing price, adjusted: **use this for returns**", "RY": "212.36"},
        {"VARIABLE": "nasdaq_volume", "Meaning": "Shares traded on **Nasdaq venues only**", "RY": "78,117"},
    ],
    hide_index=True,
)

st.markdown(f"#### `{WATCHLIST}`")
st.markdown("**Grain:** one row per ticker. Join on `TICKER`.")
st.table(
    [
        {"TICKER": "NDAQ", "COMPANY_NAME": "Nasdaq Inc.", "SEGMENT": "Exchange operator", "Listing": "Nasdaq"},
        {"TICKER": "ICE", "COMPANY_NAME": "Intercontinental Exchange", "SEGMENT": "Exchange operator", "Listing": "NYSE"},
        {"TICKER": "CME", "COMPANY_NAME": "CME Group", "SEGMENT": "Exchange operator", "Listing": "Nasdaq"},
        {"TICKER": "CBOE", "COMPANY_NAME": "Cboe Global Markets", "SEGMENT": "Exchange operator", "Listing": "Cboe BZX"},
        {"TICKER": "RY", "COMPANY_NAME": "Royal Bank of Canada", "SEGMENT": "Canadian interlisted", "Listing": "NYSE"},
        {"TICKER": "TD", "COMPANY_NAME": "Toronto-Dominion Bank", "SEGMENT": "Canadian interlisted", "Listing": "NYSE"},
        {"TICKER": "BMO", "COMPANY_NAME": "Bank of Montreal", "SEGMENT": "Canadian interlisted", "Listing": "NYSE"},
        {"TICKER": "BNS", "COMPANY_NAME": "Bank of Nova Scotia", "SEGMENT": "Canadian interlisted", "Listing": "NYSE"},
        {"TICKER": "ENB", "COMPANY_NAME": "Enbridge", "SEGMENT": "Canadian interlisted", "Listing": "NYSE"},
        {"TICKER": "CNQ", "COMPANY_NAME": "Canadian Natural Resources", "SEGMENT": "Canadian interlisted", "Listing": "NYSE"},
        {"TICKER": "SHOP", "COMPANY_NAME": "Shopify", "SEGMENT": "Canadian interlisted", "Listing": "NYSE"},
        {"TICKER": "SPY", "COMPANY_NAME": "SPDR S&P 500 ETF", "SEGMENT": "Benchmark ETF", "Listing": "NYSE Arca"},
        {"TICKER": "QQQ", "COMPANY_NAME": "Invesco QQQ (Nasdaq-100) ETF", "SEGMENT": "Benchmark ETF", "Listing": "Nasdaq"},
        {"TICKER": "EWC", "COMPANY_NAME": "iShares MSCI Canada ETF", "SEGMENT": "Benchmark ETF", "Listing": "NYSE Arca"},
    ],
    hide_index=True,
)
st.caption("The Listing column is from PRIMARY_EXCHANGE_NAME in the prices table; it isn't stored in WATCHLIST.")

st.markdown("#### Traps to avoid")
st.table(
    [
        {"Trap": "Aggregating without filtering `VARIABLE`", "Symptom": "Averages mix prices and share counts; row counts are 9× too high", "Fix": "Filter to one variable, or pivot first"},
        {"Trap": "Returns on raw close", "Symptom": "Dividend payers (banks, ENB) look worse than they did", "Fix": "Use `post-market_close_adjusted`"},
        {"Trap": "Calling `nasdaq_volume` total volume", "Symptom": "NYSE-listed names look thinly traded", "Fix": "Compare volume over time for one ticker, not across tickers"},
        {"Trap": "Assuming latest means today", "Symptom": "*YTD* silently ends in August", "Fix": "Always show the as-of date (2026-08-12)"},
        {"Trap": "Treating it as TSX data", "Symptom": "USD prices for Canadian banks", "Fix": "These are US listings. Say so in every output."},
    ],
    hide_index=True,
)

st.markdown("#### Starter queries")
st.code(
    """-- Shape of the data
SELECT COUNT(*) AS n_rows, COUNT(DISTINCT ticker) AS tickers,
       COUNT(DISTINCT date) AS trading_days, MIN(date), MAX(date)
FROM TMX_COCO_HOL.SOURCE.STOCK_PRICE_TIMESERIES;

-- Long to wide: one row per ticker and date
SELECT ticker, date,
       MAX(IFF(variable = 'post-market_close_adjusted', value, NULL)) AS adj_close,
       MAX(IFF(variable = 'nasdaq_volume', value, NULL))              AS nasdaq_volume
FROM TMX_COCO_HOL.SOURCE.STOCK_PRICE_TIMESERIES
WHERE ticker = 'RY' AND date >= '2026-08-01'
GROUP BY ticker, date
ORDER BY date;""",
    language="sql",
)

st.markdown(
    "Source documentation: [Snowflake Curated Data: stocks](https://data-docs.snowflake.com/sources/stocks)."
)
