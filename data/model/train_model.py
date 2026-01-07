import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import os

data = pd.read_csv("data/sample_logs.csv")

X = data[['bytes']]

model = IsolationForest(contamination=0.25, random_state=42)
model.fit(X)

os.makedirs("model", exist_ok=True)
joblib.dump(model, "model/anomaly_model.pkl")

print("Model trained successfully")
