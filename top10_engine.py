# modules/top10_engine.py
import streamlit as st
import pandas as pd

def render_top10_tables():
    # Example dummy data
    stocks = pd.DataFrame({
        "Symbol": ["ON", "AMD", "NVDA", "QUBT", "ENPH", "AAPL", "TSLA", "MSFT", "META", "GOOGL"],
        "Recommendation": ["Buy"]*10,
        "Expected Change": ["+22%", "+18%", "+17%", "+15%", "+14%", "+13%", "+12%", "+11%", "+10%", "+9%"],
        "Time Horizon": ["10 days"]*10
    })
    st.subheader("📈 Top 10 Stocks")
    st.dataframe(stocks)