# main_app.py
import streamlit as st
from modules.graph_engine import render_graph
from modules.top10_engine import render_top10_tables
from modules.utils import get_data

st.set_page_config(page_title="AI Analyzer", layout="wide", page_icon="📈")

st.title("🚀 AI-Powered Market Analyzer")

symbol = st.text_input("Enter Symbol (e.g. AAPL, BTC-USD):", "AAPL")

if symbol:
    data = get_data(symbol)
    if data is not None:
        render_graph(symbol, data)
    else:
        st.error("Failed to load data.")

render_top10_tables()