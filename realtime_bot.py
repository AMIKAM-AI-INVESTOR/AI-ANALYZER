import yfinance as yf
from pattern_recognition import detect_head_and_shoulders, detect_flags
from ai_model import train_basic_ai_model, predict_signal
from ai_model_trained_from_memory import train_model_from_memory, predict_from_memory_model

def analyze_symbol(symbol):
    try:
        df = yf.download(symbol, period="1mo")
        if df.empty or len(df) < 10:
            return f"❌ No data available for {symbol}."

        df.dropna(inplace=True)
        patterns = detect_head_and_shoulders(df) + detect_flags(df)
        pattern_names = list(set([p[1] for p in patterns]))

        ai_model = train_basic_ai_model(df)
        ai_result = predict_signal(ai_model, df)

        memory_model = train_model_from_memory()
        close_price = df["Close"].iloc[-1]
        recent_pct = (close_price - df["Close"].iloc[-5]) / df["Close"].iloc[-5]
        risk = predict_from_memory_model(memory_model, float(close_price), float(recent_pct))

        message = f"📊 **Analysis for {symbol.upper()}**\n"
        message += f"🔹 Current Price: {close_price:.2f}\n"
        message += f"🔹 Detected Patterns: {', '.join(pattern_names) if pattern_names else 'None'}\n"
        message += f"🔹 AI Forecast: {ai_result}\n"
        message += f"🔹 Risk Level (based on memory): {risk}\n"

        return message
    except Exception as e:
        return f"⚠️ Error analyzing {symbol}: {e}"
