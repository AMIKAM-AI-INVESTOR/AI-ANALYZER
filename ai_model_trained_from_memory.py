
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import os

def train_model_from_memory(file_path="memory_log.csv"):
    if not os.path.exists(file_path):
        print("No memory log found.")
        return None

    df = pd.read_csv(file_path)
    if df.empty or "pct_change" not in df or "success" not in df:
        print("Memory log missing required data.")
        return None

    # Prepare features and labels
    df["label"] = df["success"].astype(int)
    X = df[["entry_price", "pct_change"]]
    y = df["label"]

    model = DecisionTreeClassifier(max_depth=4)
    model.fit(X, y)
    return model

def predict_from_memory_model(model, entry_price, pct_change):
    if model is None:
        return "Unknown"
    X_new = pd.DataFrame([[entry_price, pct_change]], columns=["entry_price", "pct_change"])
    prediction = model.predict(X_new)[0]
    return "Likely Success" if prediction == 1 else "Likely Fail"
