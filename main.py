
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime, timedelta

st.set_page_config(page_title="AI Crypto Analyzer", layout="wide", page_icon="📊")
st.title("🚀 AI-Powered Analyzer: Top Opportunities")

# Load data
def load_data(ticker):
    end = datetime.today()
    start = end - timedelta(days=365 * 5)
    df = yf.download(ticker, start=start, end=end)
    if df.empty:
        return None
    df.dropna(inplace=True)
    return df

# Plotting function
def plot_chart(df, ticker):
    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name='Candlestick')])
    fig.update_layout(title=f"Candlestick Chart - {ticker}",
                      xaxis_title="Date", yaxis_title="Price",
                      template="plotly_dark", height=600)
    st.plotly_chart(fig, use_container_width=True)

# Top 10 Example Data (will be generated dynamically in final version)
top_stocks = pd.DataFrame({
    "Symbol": ["AAPL", "MSFT", "QUBT", "TSLA", "NVDA", "AMD", "ON", "META", "GOOGL", "AMZN"],
    "Current Price": [190.5, 310.2, 12.3, 250.0, 1100.0, 160.0, 50.3, 325.0, 145.6, 135.2],
    "Target Price": [210.0, 340.0, 16.8, 270.0, 1250.0, 180.0, 58.0, 355.0, 165.0, 150.0],
    "Expected Change (%)": [10.2, 9.6, 36.6, 8.0, 13.6, 12.5, 15.3, 9.2, 13.3, 11.1],
    "Target in (days)": [30, 40, 60, 35, 50, 30, 25, 45, 40, 35]
})

st.subheader("📊 Top 10 Stock Opportunities")
st.dataframe(top_stocks, use_container_width=True)

# Allow user to search and view a specific stock
ticker = st.text_input("Enter a stock symbol to analyze:", "AAPL")
df = load_data(ticker)
if df is not None:
    plot_chart(df, ticker)
else:
    st.warning("Data not available. Please check the symbol.")
