import pandas as pd

def generate_explanation(df):
    try:
        latest_close = df['Close'].iloc[-1]
        ma5 = df['ma5'].iloc[-1]
        ma20 = df['ma20'].iloc[-1]
        std = df['std'].iloc[-1]

        explanation_parts = []

        # ניתוח מגמה
        if pd.notna(latest_close) and pd.notna(ma5) and pd.notna(ma20):
            if latest_close > ma5 and ma5 > ma20:
                explanation_parts.append("מגמת עלייה (MA5 > MA20)")
            elif latest_close < ma5 and ma5 < ma20:
                explanation_parts.append("מגמת ירידה (MA5 < MA20)")
            else:
                explanation_parts.append("אין מגמה ברורה")
        else:
            explanation_parts.append("נתונים חלקיים לממוצעים")

        # ניתוח תנודתיות
        if pd.notna(std) and pd.notna(latest_close):
            if std < 0.02 * latest_close:
                explanation_parts.append("תנודתיות נמוכה")
            else:
                explanation_parts.append("תנודתיות גבוהה")
        else:
            explanation_parts.append("אין מספיק מידע על תנודתיות")

        return " | ".join(explanation_parts)

    except Exception as e:
        return f"שגיאה ביצירת הסבר: {str(e)}"
