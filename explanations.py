import pandas as pd

def generate_explanation(df):
    latest_close = df['Close'].iloc[-1] if not df['Close'].empty else None
    ma5 = df['ma5'].iloc[-1] if not df['ma5'].empty else None
    ma20 = df['ma20'].iloc[-1] if not df['ma20'].empty else None
    std = df['std'].iloc[-1] if not df['std'].empty else None

    explanation_parts = []

    # בדיקה שכל הנתונים קיימים ולא NaN
    if all(x is not None and pd.notna(x) for x in [latest_close, ma5, ma20]):
        if latest_close > ma5 and ma5 > ma20:
            explanation_parts.append("מגמת עלייה (MA5 > MA20)")
        elif latest_close < ma5 and ma5 < ma20:
            explanation_parts.append("מגמת ירידה (MA5 < MA20)")
        else:
            explanation_parts.append("אין מגמה ברורה")
    else:
        explanation_parts.append("נתונים חלקיים לממוצעים")

    if std is not None and pd.notna(std) and latest_close is not None and pd.notna(latest_close):
        if std < 0.02 * latest_close:
            explanation_parts.append("תנודתיות נמוכה")
        else:
            explanation_parts.append("תנודתיות גבוהה")
    else:
        explanation_parts.append("אין מספיק מידע על תנודתיות")

    return " | ".join(explanation_parts)
