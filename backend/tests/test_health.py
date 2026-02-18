from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health_root():
    resp = client.get("/")
    assert resp.status_code == 200
    assert "status" in resp.json() or resp.text != ""
