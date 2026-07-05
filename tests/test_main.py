import os
import logging
import pytest
from fastapi.testclient import TestClient

# Set env var for test DB before importing app components that use it.
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'

from main import app
from database import Base, engine


@pytest.fixture(scope="module")
def client():
    # TestClient runs app startup events.
    # Our startup event creates tables.
    with TestClient(app) as c:
        yield c
    # Drop all tables after tests are done
    Base.metadata.drop_all(bind=engine)


def test_health_endpoint_returns_200_ok(client):
    """Accessing the '/health' endpoint via an HTTP GET request returns a 200 OK status."""
    response = client.get("/health")
    assert response.status_code == 200


def test_no_sensitive_data_logged(client, caplog):
    """Review of application logs confirms that no sensitive data is logged during normal operation."""
    with caplog.at_level(logging.INFO):
        # Make a request with potentially sensitive headers
        headers = {
            "Authorization": "Bearer super-secret-token",
            "X-Custom-Sensitive-Header": "secret-value",
        }
        client.get("/health", headers=headers)

    # Uvicorn access logs by default do not include headers.
    # This test verifies that behavior.
    log_text = caplog.text
    assert "super-secret-token" not in log_text
    assert "secret-value" not in log_text
