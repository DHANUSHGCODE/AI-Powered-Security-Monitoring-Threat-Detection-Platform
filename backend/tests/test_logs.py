import pytest
from fastapi.testclient import TestClient
from backend.main import app


VALID_PAYLOAD = {
    "source_ip": "10.0.0.1",
    "destination_ip": "10.0.0.2",
    "protocol": "TCP",
    "bytes_transferred": 1234,
    "event_type": "normal",
    "details": "test log entry"
}


# --- POST /logs/ Tests ---

def test_create_log_success(client):
    """Test POST /logs/ with a valid payload returns 200 or 201."""
    resp = client.post("/logs/", json=VALID_PAYLOAD)
    assert resp.status_code in (200, 201), f"Expected 200/201, got {resp.status_code}"
    data = resp.json()
    assert isinstance(data, dict)


def test_create_log_missing_required_field(client):
    """Test POST /logs/ with missing required field returns 422 Unprocessable Entity."""
    payload = {
        "destination_ip": "10.0.0.2",
        "protocol": "TCP",
        "bytes_transferred": 1234,
        "event_type": "normal"
        # source_ip is missing
    }
    resp = client.post("/logs/", json=payload)
    assert resp.status_code == 422, f"Expected 422, got {resp.status_code}"


def test_create_log_invalid_payload_empty_body(client):
    """Test POST /logs/ with empty body returns 422."""
    resp = client.post("/logs/", json={})
    assert resp.status_code == 422, f"Expected 422, got {resp.status_code}"


def test_create_log_invalid_data_type(client):
    """Test POST /logs/ with wrong data type for bytes_transferred returns 422."""
    payload = {**VALID_PAYLOAD, "bytes_transferred": "not_a_number"}
    resp = client.post("/logs/", json=payload)
    assert resp.status_code == 422, f"Expected 422, got {resp.status_code}"


def test_create_log_response_structure(client):
    """Test POST /logs/ response has expected fields."""
    resp = client.post("/logs/", json=VALID_PAYLOAD)
    assert resp.status_code in (200, 201)
    data = resp.json()
    assert "id" in data
    assert "timestamp" in data
    assert "source_ip" in data


# --- GET /logs/ Tests ---

def test_get_logs(client):
    """Test GET /logs/ returns a list."""
    resp = client.get("/logs/")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)


def test_get_logs_with_pagination(client):
    """Test GET /logs/ with skip and limit parameters."""
    resp = client.get("/logs/?skip=0&limit=5")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) <= 5
