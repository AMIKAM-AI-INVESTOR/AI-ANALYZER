
import yfinance as yf
import pandas as pd

def run_backtest(ticker_symbol):
    try:
        ticker = yf.Ticker(ticker_symbol)
        hist = ticker.history(period="6mo", interval="1d")
        if hist.empty:
            return "⚠️ No historical data available."

        data = hist.copy()
        data['Signal'] = None

        for i in range(1, len(data) - 1):
            if data['Close'].iloc[i] > data['Close'].iloc[i - 1] * 1.04:
                data.at[data.index[i], 'Signal'] = 'BUY'
            elif data['Close'].iloc[i] < data['Close'].iloc[i - 1] * 0.96:
                data.at[data.index[i], 'Signal'] = 'SELL'

        if 'Signal' not in data.columns or data['Signal'].isnull().all():
            return "⚠️ No valid trade signals found."

        buy_signals = data[data['Signal'] == 'BUY']
        sell_signals = data[data['Signal'] == 'SELL']

        results = {
            "Total BUY signals": len(buy_signals),
            "Total SELL signals": len(sell_signals),
            "BUY dates": buy_signals.index.strftime('%Y-%m-%d').tolist(),
            "SELL dates": sell_signals.index.strftime('%Y-%m-%d').tolist(),
        }
        return results

    except Exception as e:
        return f"❌ Error during backtest: {e}"
