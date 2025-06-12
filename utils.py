import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# זיהוי אותות קנייה/מכירה פשוטים
def detect_trade_signals(df, threshold=0.03):
    signals = []
    for i in range(1, len(df)):
        if df["Close"].iloc[i] > df["Close"].iloc[i - 1] * (1 + threshold):
            signals.append("Buy")
        elif df["Close"].iloc[i] < df["Close"].iloc[i - 1] * (1 - threshold):
            signals.append("Sell")
        else:
            signals.append("")
    signals.insert(0, "")
    df["Signal"] = signals
    return df

# הצגת גרף נרות יפניים
def display_candlestick_chart(df, title):
    fig = go.Figure(data=[
        go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name="Candlesticks"
        )
    ])
    
    buy_signals = df[df["Signal"] == "Buy"]
    sell_signals = df[df["Signal"] == "Sell"]

    fig.add_trace(go.Scatter(
        x=buy_signals.index,
        y=buy_signals["Close"],
        mode="markers",
        marker=dict(symbol="triangle-up", color="green", size=10),
        name="Buy Signal"
    ))

    fig.add_trace(go.Scatter(
        x=sell_signals.index,
        y=sell_signals["Close"],
        mode="markers",
        marker=dict(symbol="triangle-down", color="red", size=10),
        name="Sell Signal"
    ))

    fig.update_layout(title=title, xaxis_title="Date", yaxis_title="Price")
    st.plotly_chart(fig, use_container_width=True)

# הצגת טבלת Top 10 תחזיות
def display_top_10_forecast_table(df, asset_type):
    top_df = df.sort_values("תחזית (%)", ascending=False).head(10)
    st.subheader(f"📈 Top 10 {asset_type} מומלצות")
    st.dataframe(top_df, use_container_width=True)
