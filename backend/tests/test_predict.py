from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_predict_endpoint():
    payload = {
        "source_ip": "10.0.0.1",
        "destination_ip": "10.0.0.2",
        "protocol": "TCP",
        "bytes_transferred": 1000,
        "event_type": "normal",
        "details": "test prediction"
    }
    resp = client.post("/predict/", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert "is_anomaly" in body
