
def generate_explanation(df):
    latest_close = df['Close'].iloc[-1]
    ma5 = df['ma5'].iloc[-1]
    ma20 = df['ma20'].iloc[-1]

    explanation_parts = []

    if latest_close > ma5 and ma5 > ma20:
        explanation_parts.append("מגמת עלייה (MA5 > MA20)")
    elif latest_close < ma5 and ma5 < ma20:
        explanation_parts.append("מגמת ירידה (MA5 < MA20)")
    else:
        explanation_parts.append("אין מגמה ברורה")

    std = df['std'].iloc[-1]
    if std < 0.02 * latest_close:
        explanation_parts.append("תנודתיות נמוכה")
    else:
        explanation_parts.append("תנודתיות גבוהה")

    return " | ".join(explanation_parts)
