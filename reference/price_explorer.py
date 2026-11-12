"""TMX CoCo HOL reference app: read-only price and volume explorer over your Iceberg table.

Reference solution for exercise 5. Set PRICES to your table. Uses only packages bundled
with the Streamlit container runtime; no external access integration required.
"""

import pandas as pd
import streamlit as st

PRICES = "DEV_EDX_HACKATHONTOR_<TEAM>_DB.CONSUMER.STOCK_PRICE_TIMESERIES_<INITIALS>"
DEFAULT_TICKERS = ["NDAQ", "ICE", "CME", "CBOE"]

st.set_page_config(page_title="US stock price explorer", layout="wide")
conn = st.connection("snowflake")


@st.cache_data(ttl=3600)
def load_universe() -> pd.DataFrame:
    return conn.query(
        f"SELECT TICKER, MIN(DATE) AS MIN_D, MAX(DATE) AS MAX_D FROM {PRICES} GROUP BY TICKER ORDER BY TICKER"
    )


@st.cache_data(ttl=3600)
def load_daily(tickers: tuple, start, end) -> pd.DataFrame:
    # Tickers come only from the table itself (allow-list); dates are date objects.
    ticker_list = ", ".join(f"'{t}'" for t in tickers if t in allowed)
    sql = f"""
        SELECT TICKER, DATE,
               MAX(IFF(VARIABLE = 'post-market_close_adjusted', VALUE, NULL)) AS ADJ_CLOSE,
               MAX(IFF(VARIABLE = 'nasdaq_volume', VALUE, NULL))             AS NASDAQ_VOLUME
        FROM {PRICES}
        WHERE TICKER IN ({ticker_list})
          AND DATE BETWEEN '{start.isoformat()}' AND '{end.isoformat()}'
          AND VARIABLE IN ('post-market_close_adjusted', 'nasdaq_volume')
        GROUP BY TICKER, DATE
        ORDER BY TICKER, DATE
    """
    return conn.query(sql)


universe = load_universe()
allowed = set(universe["TICKER"])
min_d = pd.to_datetime(universe["MIN_D"]).min().date()
max_d = pd.to_datetime(universe["MAX_D"]).max().date()

st.title("US stock price explorer")
st.caption(
    f"Source: your Iceberg copy of Snowflake Curated Data (Free), US listings in USD. Latest available date: {max_d}. "
    "The free tier lags about three months. Volume is Nasdaq-venue volume, not consolidated volume."
)

with st.sidebar:
    tickers = st.multiselect(
        "Tickers",
        sorted(allowed),
        default=[t for t in DEFAULT_TICKERS if t in allowed],
        max_selections=10,
    )
    picked = st.date_input("Date range", value=(min_d, max_d), min_value=min_d, max_value=max_d)

if not tickers:
    st.info("Pick at least one ticker.")
    st.stop()
if not isinstance(picked, tuple) or len(picked) != 2:
    st.info("Pick a start and end date.")
    st.stop()
start, end = picked

df = load_daily(tuple(tickers), start, end)
df["DATE"] = pd.to_datetime(df["DATE"])
df = df.sort_values(["TICKER", "DATE"])
df["INDEXED"] = df.groupby("TICKER")["ADJ_CLOSE"].transform(lambda s: 100 * s / s.iloc[0])

summary = (
    df.groupby("TICKER")
    .agg(first_close=("ADJ_CLOSE", "first"), last_close=("ADJ_CLOSE", "last"), avg_volume=("NASDAQ_VOLUME", "mean"))
    .assign(return_pct=lambda t: 100 * (t["last_close"] / t["first_close"] - 1))
    .reset_index()
)

cols = st.columns(len(summary))
for col, row in zip(cols, summary.itertuples()):
    col.metric(row.TICKER, f"${row.last_close:,.2f}", f"{row.return_pct:+.1f}%")

st.subheader("Adjusted close, indexed to 100 at start of range")
st.line_chart(df, x="DATE", y="INDEXED", color="TICKER")

st.subheader("Daily Nasdaq-venue volume")
st.bar_chart(df, x="DATE", y="NASDAQ_VOLUME", color="TICKER")

with st.expander("Data"):
    st.dataframe(summary, hide_index=True)
