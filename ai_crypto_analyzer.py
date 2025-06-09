import streamlit as st
from top10_data import get_top10_predictions
from utils import fetch_price_history, detect_trade_signals
from backtesting import run_backtesting
from fundamentals import get_fundamental_data
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.title("AI Crypto & Stock Analyzer 📈🤖")

ticker = st.text_input("Enter Ticker Symbol (e.g., AAPL or BTC-USD):")

if ticker:
    df = fetch_price_history(ticker)
    if not df.empty:
        df = detect_trade_signals(df)

        st.subheader("Price Chart with Buy/Sell Signals")

        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='Candlestick'
        ))

        buy_signals = df[df['Signal'] == 'Buy']
        sell_signals = df[df['Signal'] == 'Sell']

        fig.add_trace(go.Scatter(x=buy_signals.index, y=buy_signals['Close'],
                                 mode='markers', marker=dict(color='green', size=10),
                                 name='Buy Signal'))

        fig.add_trace(go.Scatter(x=sell_signals.index, y=sell_signals['Close'],
                                 mode='markers', marker=dict(color='red', size=10),
                                 name='Sell Signal'))

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Backtesting Results")
        results = run_backtesting(df)
        st.dataframe(results)

        st.subheader("Fundamental Data")
        fund_data = get_fundamental_data(ticker)
        st.json(fund_data)
    else:
        st.error("No data found for the provided ticker.")

st.sidebar.header("Top 10 Predictions")
top10_df = get_top10_predictions()
st.sidebar.dataframe(top10_df)
