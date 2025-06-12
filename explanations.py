import pandas as pd

def generate_explanation(df):
    explanation_parts = []

    try:
        latest_close = df['Close'].iloc[-1]
        ma5 = df['ma5'].iloc[-1]
        ma20 = df['ma20'].iloc[-1]
        std = df['std'].iloc[-1]
    except Exception:
        return "שגיאה: אין מספיק נתונים לניתוח"

    try:
        # ניתוח ממוצעים נעים
        if pd.notna(latest_close) and pd.notna(ma5) and pd.notna(ma20):
            if float(latest_close) > float(ma5) > float(ma20):
                explanation_parts.append("מגמת עלייה (MA5 > MA20)")
            elif float(latest_close) < float(ma5) < float(ma20):
                explanation_parts.append("מגמת ירידה (MA5 < MA20)")
            else:
                explanation_parts.append("אין מגמה ברורה")
        else:
            explanation_parts.append("נתונים חלקיים על ממוצעים נעים")

        # ניתוח תנודתיות
        if pd.notna(std) and pd.notna(latest_close):
            if float(std) < 0.02 * float(latest_close):
                explanation_parts.append("תנודתיות נמוכה")
            else:
                explanation_parts.append("תנודתיות גבוהה")
        else:
            explanation_parts.append("אין מספיק מידע על תנודתיות")

    except Exception:
        explanation_parts.append("שגיאה בעיבוד הניתוח")

    return " | ".join(explanation_parts)
