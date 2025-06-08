# modules/graph_engine.py
import streamlit as st
import plotly.graph_objs as go

def render_graph(symbol, df):
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'],
                                 low=df['Low'], close=df['Close'], name=symbol))
    st.plotly_chart(fig, use_container_width=True)