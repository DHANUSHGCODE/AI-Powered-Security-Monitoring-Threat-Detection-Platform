import pytest
from fastapi.testclient import TestClient
from backend.main import app


def test_health_root(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert "message" in resp.json()
