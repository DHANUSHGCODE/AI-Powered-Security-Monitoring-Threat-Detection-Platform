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
    # Accept 200 (model loaded) or 503 (model not available in test env)
    assert resp.status_code in (200, 503)
    if resp.status_code == 200:
        body = resp.json()
        assert "is_anomaly" in body
