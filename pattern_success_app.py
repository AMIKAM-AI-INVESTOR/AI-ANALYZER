
import streamlit as st
import pandas as pd
from multi_asset_trainer import train_on_multiple_symbols
from pattern_success_stats import summarize_pattern_stats

st.set_page_config(layout="wide", page_title="Pattern Success Summary")
st.title("📊 Pattern Success Rates Across Multiple Assets")

symbols = st.text_input("Enter stock/crypto symbols separated by commas", value="AAPL,MSFT,GOOG,NVDA,TSLA,BTC-USD,ETH-USD")
symbol_list = [s.strip() for s in symbols.split(",") if s.strip()]

if st.button("Run Pattern Analysis"):
    with st.spinner("Fetching data and analyzing patterns..."):
        stats_df = train_on_multiple_symbols(symbol_list)
        if stats_df.empty:
            st.warning("No patterns were detected for the selected symbols.")
        else:
            summary_df = summarize_pattern_stats(stats_df)
            st.success("Pattern analysis complete!")
            st.dataframe(summary_df, use_container_width=True)
