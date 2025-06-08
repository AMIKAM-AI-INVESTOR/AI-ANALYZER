
import pandas as pd
import plotly.graph_objs as go

def plot_price_chart(data):
    if data is None or not isinstance(data, pd.DataFrame) or 'signal' not in data.columns:
        import streamlit as st
        st.error("No valid data available for chart.")
        return None

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['Close'],
        mode='lines',
        name='Close Price'
    ))

    buy_signals = data[data['signal'] == 'BUY']
    sell_signals = data[data['signal'] == 'SELL']

    fig.add_trace(go.Scatter(
        x=buy_signals.index,
        y=buy_signals['Close'],
        mode='markers',
        name='Buy Signal',
        marker=dict(color='green', size=10, symbol='triangle-up')
    ))

    fig.add_trace(go.Scatter(
        x=sell_signals.index,
        y=sell_signals['Close'],
        mode='markers',
        name='Sell Signal',
        marker=dict(color='red', size=10, symbol='triangle-down')
    ))

    fig.update_layout(
        title='Price Chart with Buy/Sell Signals',
        xaxis_title='Date',
        yaxis_title='Price',
        template='plotly_white'
    )

    return fig
