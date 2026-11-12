"""TMX CoCo HOL reference app: read-only price and volume explorer.

Facilitator fallback for Exercise 4. Uses only packages bundled with the
Streamlit container runtime; no external access integration required.
"""

import altair as alt
import pandas as pd
import streamlit as st

SOURCE = "TMX_COCO_HOL.SOURCE.STOCK_PRICE_TIMESERIES"
WATCHLIST = "TMX_COCO_HOL.SOURCE.WATCHLIST"

st.set_page_config(page_title="TMX HOL stock explorer", layout="wide")
conn = st.connection("snowflake")


@st.cache_data(ttl=3600)
def load_watchlist() -> pd.DataFrame:
    return conn.query(f"SELECT TICKER, COMPANY_NAME, SEGMENT FROM {WATCHLIST} ORDER BY SEGMENT, TICKER")


@st.cache_data(ttl=3600)
def load_bounds() -> pd.DataFrame:
    return conn.query(f"SELECT MIN(DATE) AS MIN_D, MAX(DATE) AS MAX_D FROM {SOURCE}")


@st.cache_data(ttl=3600)
def load_daily(tickers: tuple, start, end) -> pd.DataFrame:
    # Tickers come only from the admin-owned watchlist (allow-list); dates are date objects.
    ticker_list = ", ".join(f"'{t}'" for t in tickers if t in allowed)
    sql = f"""
        SELECT TICKER, DATE,
               MAX(IFF(VARIABLE = 'post-market_close_adjusted', VALUE, NULL)) AS ADJ_CLOSE,
               MAX(IFF(VARIABLE = 'nasdaq_volume', VALUE, NULL))             AS NASDAQ_VOLUME
        FROM {SOURCE}
        WHERE TICKER IN ({ticker_list})
          AND DATE BETWEEN '{start.isoformat()}' AND '{end.isoformat()}'
          AND VARIABLE IN ('post-market_close_adjusted', 'nasdaq_volume')
        GROUP BY TICKER, DATE
        ORDER BY TICKER, DATE
    """
    return conn.query(sql)


watchlist = load_watchlist()
allowed = set(watchlist["TICKER"])
bounds = load_bounds().iloc[0]
min_d, max_d = pd.to_datetime(bounds["MIN_D"]).date(), pd.to_datetime(bounds["MAX_D"]).date()

st.title("Price and volume explorer")
st.caption(
    f"Source: Snowflake Curated Data (Free), US listings in USD. Latest available date: {max_d}. "
    "Free tier lags about three months. Volume is Nasdaq-venue volume, not consolidated volume."
)

with st.sidebar:
    segments = st.multiselect("Segment", sorted(watchlist["SEGMENT"].unique()), default=["Exchange operator"])
    options = watchlist[watchlist["SEGMENT"].isin(segments)]["TICKER"].tolist()
    tickers = st.multiselect("Tickers", options, default=options[:4])
    picked = st.date_input(
        "Date range", value=(pd.Timestamp("2026-01-01").date(), max_d), min_value=min_d, max_value=max_d
    )

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
st.altair_chart(
    alt.Chart(df).mark_line().encode(x="DATE:T", y=alt.Y("INDEXED:Q", title="Index"), color="TICKER:N"),
    use_container_width=True,
)

st.subheader("Daily Nasdaq-venue volume")
st.altair_chart(
    alt.Chart(df).mark_bar().encode(x="DATE:T", y=alt.Y("NASDAQ_VOLUME:Q", title="Shares"), color="TICKER:N"),
    use_container_width=True,
)

with st.expander("Data"):
    st.dataframe(summary, hide_index=True, use_container_width=True)
