from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_log():
    payload = {
        "source_ip": "10.0.0.1",
        "destination_ip": "10.0.0.2",
        "protocol": "TCP",
        "bytes_transferred": 1234,
        "event_type": "normal",
        "details": "test log"
    }
    resp = client.post("/logs/", json=payload)
    assert resp.status_code in (200, 201)

def test_list_logs():
    resp = client.get("/logs/")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list) or isinstance(data, dict)
