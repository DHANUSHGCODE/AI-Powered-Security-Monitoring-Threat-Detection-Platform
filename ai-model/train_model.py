import os
import joblib
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "../data/generated_logs.csv")
MODEL_FILE = os.path.join(BASE_DIR, "isolation_forest_model.pkl")
ENCODERS_FILE = os.path.join(BASE_DIR, "encoders.pkl")
METRICS_FILE = os.path.join(BASE_DIR, "training_metrics.csv")


def load_data(path: str) -> pd.DataFrame:
    """Load generated logs for training."""
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Data file {path} not found. Run log_generator.py first."
        )
    df = pd.read_csv(path)
    return df


def build_features(df: pd.DataFrame):
    """
    Encode categorical fields and build numeric feature matrix.
    Returns: features_df, encoders_dict
    """
    # Encode categorical variables: protocol, event_type
    le_protocol = LabelEncoder()
    df["protocol_encoded"] = le_protocol.fit_transform(df["protocol"])

    # Fix #9: Also save le_event encoder so it can be reused for future inference
    # Previously le_event was trained but never saved - now included in encoders.pkl
    le_event = LabelEncoder()
    df["event_encoded"] = le_event.fit_transform(df["event_type"])

    # Use 'bytes' as column name to match the prediction endpoint in main.py
    features = df[["bytes_transferred", "protocol_encoded"]].rename(
        columns={"bytes_transferred": "bytes"}
    )

    encoders = {
        "protocol": le_protocol,
        "event": le_event,
    }
    return features, encoders


def train_isolation_forest(features: pd.DataFrame) -> IsolationForest:
    """Train Isolation Forest on the provided feature matrix."""
    # contamination=0.05 means ~5% of data expected to be anomalous
    model = IsolationForest(
        n_estimators=100,
        contamination=0.05,
        random_state=42,
    )
    model.fit(features)
    return model


def evaluate_and_log_metrics(
    model: IsolationForest, features: pd.DataFrame, out_path: str
):
    """
    Run inference on the training data and write simple metrics to CSV
    for debugging and observability.
    """
    predictions = model.predict(features)
    n_anomalies = int((predictions == -1).sum())
    n_total = int(len(predictions))
    anomaly_rate = 100.0 * n_anomalies / max(n_total, 1)

    metrics_df = pd.DataFrame(
        [
            {
                "n_samples": n_total,
                "n_anomalies": n_anomalies,
                "anomaly_rate_pct": round(anomaly_rate, 2),
            }
        ]
    )
    metrics_df.to_csv(out_path, index=False)

    print(
        f"Training complete. Detected {n_anomalies}/{n_total} anomalies "
        f"({anomaly_rate:.1f}%)."
    )


def train_model():
    print("Loading data...")
    df = load_data(DATA_FILE)

    print("Building features and encoders...")
    features, encoders = build_features(df)

    print("Training Isolation Forest model...")
    model = train_isolation_forest(features)

    # Persist model
    joblib.dump(model, MODEL_FILE)
    print(f"Model saved to {MODEL_FILE}")

    # Fix #9: Save BOTH encoders - protocol AND event
    # This ensures le_event is available for future use (e.g., event-based features)
    joblib.dump(encoders, ENCODERS_FILE)
    print(f"Encoders saved to {ENCODERS_FILE}")

    # Evaluate and export metrics
    print("Evaluating on training data and exporting metrics...")
    evaluate_and_log_metrics(model, features, METRICS_FILE)
    print(f"Training metrics written to {METRICS_FILE}")

    # Simple introspection for debugging
    le_protocol = encoders["protocol"]
    le_event = encoders["event"]
    print("Protocol classes:", list(le_protocol.classes_))
    print("Event classes:", list(le_event.classes_))


if __name__ == "__main__":
    train_model()
