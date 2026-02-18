from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_log():
    payload = {
        "timestamp": "2025-01-01T00:00:00Z",
        "source_ip": "10.0.0.1",
        "destination_ip": "10.0.0.2",
        "bytes_sent": 1234,
        "bytes_received": 5678,
        "protocol": "TCP",
        "status": "OK"
    }
    resp = client.post("/logs/", json=payload)
    assert resp.status_code in (200, 201)

def test_list_logs():
    resp = client.get("/logs/")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list) or isinstance(data, dict)
