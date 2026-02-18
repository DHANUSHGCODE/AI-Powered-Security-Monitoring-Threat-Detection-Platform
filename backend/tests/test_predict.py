from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_predict_endpoint():
    payload = {
        "source_ip": "10.0.0.1",
        "destination_ip": "10.0.0.2",
        "bytes_sent": 1000,
        "bytes_received": 2000,
        "protocol": "TCP",
        "failed_login_count": 0
    }
    resp = client.post("/predict/", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    for key in ("score", "label", "confidence"):
        assert key in body
