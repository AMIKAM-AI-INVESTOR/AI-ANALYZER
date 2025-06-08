# ai_crypto_analyzer.py

import streamlit as st
from top10_data import get_top10_cryptos, get_top10_stocks
from fundamentals import get_fundamentals
from backtesting import run_backtest
from utils import plot_price_chart

st.set_page_config(page_title="AI Crypto Analyzer", layout="wide")
st.title("📈 AI Crypto & Stock Analyzer")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🔝 Top 10 Stocks")
    top10_stocks = get_top10_stocks()
    st.dataframe(top10_stocks, use_container_width=True)

with col2:
    st.subheader("💰 Top 10 Cryptos")
    top10_cryptos = get_top10_cryptos()
    st.dataframe(top10_cryptos, use_container_width=True)

st.markdown("---")

asset = st.text_input("Enter stock or crypto symbol (e.g., AAPL or BTC-USD):")

if asset:
    st.subheader(f"📊 Analysis for {asset.upper()}")

    chart = plot_price_chart(asset)
    if chart:
        st.plotly_chart(chart, use_container_width=True)
    else:
        st.warning("Chart data could not be retrieved.")

    st.markdown("### 🔍 Fundamental Analysis")
    fundamentals = get_fundamentals(asset)
    if fundamentals is not None:
        st.write(fundamentals)
    else:
        st.info("Fundamental data not available.")

    st.markdown("### 🧪 Backtest Strategy")
    backtest_result = run_backtest(asset)
    if backtest_result:
        st.write(backtest_result)
    else:
        st.info("Backtest data not available or failed to load.")
