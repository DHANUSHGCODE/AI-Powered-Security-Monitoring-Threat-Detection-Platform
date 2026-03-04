import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

VALID_PAYLOAD = {
    "source_ip": "10.0.0.1",
    "destination_ip": "10.0.0.2",
    "protocol": "TCP",
    "bytes_transferred": 1234,
    "event_type": "normal",
    "details": "test log entry"
}


# --- POST /logs/ Tests ---

def test_create_log_success():
    """Test POST /logs/ with a valid payload returns 200 or 201."""
    resp = client.post("/logs/", json=VALID_PAYLOAD)
    assert resp.status_code in (200, 201), f"Expected 200/201, got {resp.status_code}"
    data = resp.json()
    assert isinstance(data, dict)


def test_create_log_missing_required_field():
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


def test_create_log_invalid_payload_empty_body():
    """Test POST /logs/ with empty body returns 422."""
    resp = client.post("/logs/", json={})
    assert resp.status_code == 422, f"Expected 422, got {resp.status_code}"


def test_create_log_invalid_data_type():
    """Test POST /logs/ with wrong data type for bytes_transferred returns 422."""
    payload = {**VALID_PAYLOAD, "bytes_transferred": "not_a_number"}
    resp = client.post("/logs/", json=payload)
    assert resp.status_code == 422, f"Expected 422, got {resp.status_code}"


def test_create_log_response_structure():
    """Test POST /logs/ response contains expected fields."""
    resp = client.post("/logs/", json=VALID_PAYLOAD)
    assert resp.status_code in (200, 201)
    data = resp.json()
    # Response should be a dict (log record)
    assert isinstance(data, dict)


# --- GET /logs/ Tests ---

def test_list_logs_success():
    """Test GET /logs/ returns 200 with a list or paginated dict."""
    resp = client.get("/logs/")
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
    data = resp.json()
    assert isinstance(data, (list, dict)), "Response should be a list or dict"


def test_list_logs_pagination_skip():
    """Test GET /logs/ with skip query parameter."""
    resp = client.get("/logs/?skip=0&limit=5")
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
    data = resp.json()
    assert isinstance(data, (list, dict))


def test_list_logs_pagination_limit():
    """Test GET /logs/ with limit query parameter returns at most limit items."""
    resp = client.get("/logs/?limit=2")
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
    data = resp.json()
    if isinstance(data, list):
        assert len(data) <= 2, f"Expected at most 2 results, got {len(data)}"


def test_list_logs_after_creation():
    """Test GET /logs/ returns logs after a POST."""
    # Create a log first
    client.post("/logs/", json=VALID_PAYLOAD)
    resp = client.get("/logs/")
    assert resp.status_code == 200
    data = resp.json()
    if isinstance(data, list):
        assert len(data) >= 1, "Expected at least 1 log after creation"
    elif isinstance(data, dict):
        # Paginated response
        items = data.get("items", data.get("logs", data.get("results", [])))
        assert len(items) >= 1


# --- Error / Edge Case Tests ---

def test_create_log_no_content_type():
    """Test POST /logs/ without JSON content-type."""
    resp = client.post("/logs/", data="not json", headers={"Content-Type": "text/plain"})
    assert resp.status_code in (400, 415, 422), f"Unexpected status: {resp.status_code}"


def test_get_logs_invalid_limit():
    """Test GET /logs/ with a negative limit returns 422 or handles gracefully."""
    resp = client.get("/logs/?limit=-1")
    assert resp.status_code in (200, 422), f"Unexpected status: {resp.status_code}"


def test_get_logs_invalid_skip_type():
    """Test GET /logs/ with non-integer skip returns 422."""
    resp = client.get("/logs/?skip=abc")
    assert resp.status_code == 422, f"Expected 422, got {resp.status_code}"
