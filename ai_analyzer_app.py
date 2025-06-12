
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

            # Evaluate with memory-trained model
            from ai_model_trained_from_memory import train_model_from_memory, predict_from_memory_model
            trained_model = train_model_from_memory()
            try:
                recent_pct_change = (df["Close"].iloc[-1] - df["Close"].iloc[-5]) / df["Close"].iloc[-5]
                risk_eval = predict_from_memory_model(trained_model, df["Close"].iloc[-1], recent_pct_change)
                st.markdown(f"📊 **Risk Evaluation (based on past success patterns):** {risk_eval}")
            except Exception as e:
                st.warning(f"Risk evaluation failed: {e}")

            # Detect chart patterns
            patterns = detect_head_and_shoulders(df) + detect_flags(df)
            
            try:
            try:
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
            except Exception as e:
                st.warning(f"Pattern annotation failed: {e}")
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
# Add pattern annotations

            try:
            try:
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
            except Exception as e:
                st.warning(f"Pattern annotation failed: {e}")
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
            # Backtesting
            st.subheader("📉 AI Backtesting Results")
            try:
                backtest_df = run_backtesting(df)
                st.line_chart(backtest_df)

# -------------------------
# 📊 Pattern Success Summary Section
# -------------------------
st.header("📊 Pattern Success Rates (Across Assets)")

with st.expander("Click to run multi-asset pattern analysis"):
    user_symbols = st.text_input("Enter stock/crypto symbols separated by commas", value="AAPL,MSFT,NVDA,TSLA,BTC-USD,ETH-USD")
    symbols_list = [sym.strip() for sym in user_symbols.split(",") if sym.strip()]
    if st.button("Analyze Patterns"):
        from multi_asset_trainer import train_on_multiple_symbols
        from pattern_success_stats import summarize_pattern_stats

        with st.spinner("Analyzing patterns across multiple assets..."):
            stats_df = train_on_multiple_symbols(symbols_list)
            if stats_df.empty:
                st.warning("No patterns found for selected symbols.")
            else:
                summary_df = summarize_pattern_stats(stats_df)
                st.success("Pattern analysis completed!")
                st.dataframe(summary_df, use_container_width=True)


# -------------------------
# 🧠 Memory Log Summary Section
# -------------------------
st.header("🧠 Success Summary from Memory Log")

with st.expander("Click to view pattern performance from past forecasts"):
    from memory_summary import summarize_memory

    try:
        memory_df = summarize_memory()
        if memory_df.empty:
            st.info("No memory log found yet. Run pattern analysis to populate it.")
        else:
            st.success("Memory-based pattern performance loaded.")
            st.dataframe(memory_df, use_container_width=True)

# -------------------------
# 🤖 Real-Time Bot Advisor
# -------------------------
st.header("🤖 Ask the Analyzer Bot")

with st.expander("Ask a question like: What about TSLA?"):
    user_query = st.text_input("Ask about a stock or crypto symbol (e.g. TSLA, BTC-USD):", value="TSLA")
    if st.button("Analyze Now"):
        from realtime_bot import analyze_symbol
        response = analyze_symbol(user_query)
        st.markdown(response)
