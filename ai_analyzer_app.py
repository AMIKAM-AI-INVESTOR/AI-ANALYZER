
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
from datetime import datetime, timedelta

from top10_data import get_top10_forecasts
from backtesting import run_backtesting
from fundamentals import get_fundamental_data
from utils import detect_trade_signals
from pattern_recognition import detect_head_and_shoulders, detect_flags
from ai_model import train_basic_ai_model, predict_signal

st.set_page_config(layout="wide", page_title="AI Stock & Crypto Analyzer")
st.title("📊 AI Stock & Crypto Analyzer")

# Top 10 Forecast Section
st.header("📈 Top 10 Stocks Forecast")
stocks_df, crypto_df = get_top10_forecasts()

if not stocks_df.empty:
    st.dataframe(stocks_df, use_container_width=True)
else:
    st.warning("No forecast data available for stocks.")

st.header("🪙 Top 10 Cryptocurrencies Forecast")
if not crypto_df.empty:
    st.dataframe(crypto_df, use_container_width=True)
else:
    st.warning("No forecast data available for cryptocurrencies.")

# Analyze a Specific Asset
st.header("🔍 Analyze a Specific Asset")
symbol = st.text_input("Enter a stock or crypto symbol (e.g. AAPL, BTC-USD):", value="AAPL")
period = st.selectbox("Select time period:", ["1mo", "3mo", "6mo", "1y"])

if symbol:
    try:
        df = yf.download(symbol, period=period)
        if df.empty:
            st.warning("No valid data found for selected symbol or time range.")
        else:
            df.dropna(inplace=True)
            df = detect_trade_signals(df)

            
            # Train AI model
            model = train_basic_ai_model(df)
            ai_signal = predict_signal(model, df)
            st.markdown(f"### 🤖 AI Prediction: **{ai_signal}**")

            # Detect chart patterns
            patterns = detect_head_and_shoulders(df) + detect_flags(df)
            for date, pattern_name in patterns:
                st.markdown(f"🔍 Pattern Detected: **{pattern_name}** on {date.date()}")

# Candlestick chart
            st.subheader(f"{symbol} Candlestick Chart")
            fig = go.Figure(data=[
                go.Candlestick(
                    x=df.index,
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'],
                    increasing_line_color='green',
                    decreasing_line_color='red'
                )
            ])
            
# Add pattern annotations
for date, pattern_name in patterns:
    if date in df.index:
        price = df.loc[date]['High']
        fig.add_annotation(
            x=date,
            y=price,
            text=pattern_name,
            showarrow=True,
            arrowhead=1,
            ax=0,
            ay=-40,
            font=dict(color="blue"),
            bgcolor="rgba(255,255,255,0.9)"
        )

st.plotly_chart(fig, use_container_width=True)

            # Backtesting
            st.subheader("📉 AI Backtesting Results")
            try:
                backtest_df = run_backtesting(df)
                st.line_chart(backtest_df)
            except Exception as e:
                st.error(f"Backtesting failed: {str(e)}")
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
