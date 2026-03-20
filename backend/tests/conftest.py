import pytest
from fastapi.testclient import TestClient
from backend.main import app


@pytest.fixture(scope="module")
def client():
    """Provide a TestClient for all tests in this module."""
    with TestClient(app) as c:
        yield c
