import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "../data/generated_logs.csv")
MODEL_FILE = os.path.join(BASE_DIR, "isolation_forest_model.pkl")
ENCODERS_FILE = os.path.join(BASE_DIR, "encoders.pkl")

def train_model():
    if not os.path.exists(DATA_FILE):
        print(f"Data file {DATA_FILE} not found. Run log_generator.py first.")
        return

    print("Loading data...")
    df = pd.read_csv(DATA_FILE)

    # Feature Engineering
    # Encode categorical variables: Protocol, Event Type
    le_protocol = LabelEncoder()
    df['protocol_encoded'] = le_protocol.fit_transform(df['protocol'])

    # Fix #9: Also save le_event encoder so it can be reused for future inference
    # Previously le_event was trained but never saved - now it is included in encoders.pkl
    le_event = LabelEncoder()
    df['event_encoded'] = le_event.fit_transform(df['event_type'])

    # Select features for Isolation Forest
    # Using bytes_transferred and protocol_encoded as primary anomaly indicators
    features = df[['bytes_transferred', 'protocol_encoded']].rename(
        columns={'bytes_transferred': 'bytes', 'protocol_encoded': 'protocol_encoded'}
    )

    print("Training Isolation Forest model...")
    # contamination=0.05 means ~5% of data expected to be anomalous
    model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
    model.fit(features)

    # Save model
    joblib.dump(model, MODEL_FILE)
    print(f"Model saved to {MODEL_FILE}")

    # Fix #9: Save BOTH encoders - protocol AND event
    # This ensures le_event is available for future use (e.g., event-based features)
    joblib.dump({
        'protocol': le_protocol,
        'event': le_event,
    }, ENCODERS_FILE)
    print(f"Encoders saved to {ENCODERS_FILE}")

    # Evaluate on training data
    predictions = model.predict(features)
    n_anomalies = (predictions == -1).sum()
    n_total = len(predictions)
    print(f"Training complete. Detected {n_anomalies}/{n_total} anomalies ({100*n_anomalies/n_total:.1f}%)")
    print("Protocol classes:", list(le_protocol.classes_))
    print("Event classes:", list(le_event.classes_))

if __name__ == "__main__":
    train_model()
