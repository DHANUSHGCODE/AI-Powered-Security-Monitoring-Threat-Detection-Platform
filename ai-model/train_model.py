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

    le_event = LabelEncoder()
    df['event_encoded'] = le_event.fit_transform(df['event_type']) # In real scenario, we might not have 'event_type' for new anomalies, but for this demo we rely on patterns
    
    # We will use Source IP as a feature? IP addresses are categorical but high cardinality.
    # For a simple anomaly detection, let's look at Bytes and Protocol.
    # A better approach for IPs is frequency encoding or just ignoring specific IPs and looking at behavior.
    # Let's use Bytes and Protocol for simplicity for now.
    
    features = ['bytes', 'protocol_encoded']
    X = df[features]

    print("Training Isolation Forest...")
    # Contamination is the expected proportion of outliers
    clf = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
    clf.fit(X)

    # Save model and encoders
    print("Saving model...")
    joblib.dump(clf, MODEL_FILE)
    joblib.dump({'protocol': le_protocol}, ENCODERS_FILE)
    print("Model trained and saved successfully.")

if __name__ == "__main__":
    train_model()
