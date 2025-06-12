
import yfinance as yf
from pattern_recognition import detect_head_and_shoulders, detect_flags
from ai_model import train_basic_ai_model, predict_signal
from ai_model_trained_from_memory import train_model_from_memory, predict_from_memory_model

def check_alert(symbol):
    df = yf.download(symbol, period="1mo")
    if df.empty or len(df) < 10:
        return None

    df.dropna(inplace=True)
    patterns = detect_head_and_shoulders(df) + detect_flags(df)

    model = train_basic_ai_model(df)
    ai_forecast = predict_signal(model, df)

    memory_model = train_model_from_memory()
    try:
        recent_pct = (df["Close"].iloc[-1] - df["Close"].iloc[-5]) / df["Close"].iloc[-5]
        risk_result = predict_from_memory_model(memory_model, df["Close"].iloc[-1], recent_pct)
    except:
        risk_result = "Unknown"

    if patterns and ai_forecast == "Buy" and risk_result == "Likely Success":
        return {
            "symbol": symbol,
            "pattern": patterns[-1][1],
            "ai_forecast": ai_forecast,
            "risk": risk_result,
            "price": df["Close"].iloc[-1],
            "date": df.index[-1].date().isoformat()
        }

    return None
