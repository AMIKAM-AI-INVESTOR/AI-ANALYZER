from utils import (
    detect_trade_signals,
    display_candlestick_chart,
    display_top_10_forecast_table,
    display_backtest_results,
    display_asset_analysis,
)
import datetime

st.set_page_config(layout="wide", page_title="AI Stock & Crypto Analyzer - תחזיות חכמות")

st.title("📊 AI Stock & Crypto Analyzer - תחזיות חכמות")

tab1, tab2 = st.tabs(["🔍 ניתוח לפי סימול בודד", "📈 Top 10 מניות מומלצות"])

with tab1:
    st.header("🔎 ניתוח לפי סימול בודד")
    symbol = st.text_input("הכנס סימול (לדוגמה: AAPL או BTC-USD):")

    if st.button("בצע ניתוח") and symbol:
        result, error = analyze_asset(symbol)
        if error:
            st.error(error)
        else:
            display_candlestick_chart(result)
            display_backtest_results(result)
            display_asset_analysis(result)

with tab2:
    st.header("📈 Top 10 מניות מומלצות")
    try:
        df_stocks = analyze_with_model(train_model(stock_symbols, "מניה"), stock_symbols, "מניה")
        df_crypto = analyze_with_model(train_model(crypto_symbols, "קריפטו"), crypto_symbols, "קריפטו")

        display_top_10_forecast_table(df_stocks, "Top 10 מניות מומלצות")
        display_top_10_forecast_table(df_crypto, "Top 10 מטבעות מומלצים")
    except Exception as e:
        st.error(f"שגיאה בעת עיבוד התחזיות: {e}")

def analyze_asset(symbol):
    try:
        df = fetch_data(symbol)
        df = detect_trade_signals(df)
        explanation = generate_explanation(df)
        df["explanation"] = explanation
        return df, None
    except Exception as e:
        return None, str(e)
