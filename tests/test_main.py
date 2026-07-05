import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import OperationalError
import sqlalchemy

# This needs to be set *before* other modules are imported.
os.environ['DATABASE_URL'] = 'postgresql://user:password@localhost/test_db'

from main import app, on_startup
from models import Base
from database import engine

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """
    Fixture to set up the test database. It assumes the 'test_db' database exists on localhost.
    It runs the app's startup logic to create tables, and drops them after tests.
    """
    try:
        # Test the connection
        connection = engine.connect()
        connection.close()
    except OperationalError as e:
        pytest.fail(f"Could not connect to test database 'test_db' on localhost. "
                    f"Please ensure it exists and the credentials are correct. Error: {e}")

    # Create tables using the app's startup logic
    on_startup()
    
    yield
    
    # Teardown: drop all tables
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session")
def client():
    """Provides a TestClient for the app."""
    with TestClient(app) as c:
        yield c

def test_app_starts(client):
    """[AC] The FastAPI application starts successfully without any errors."""
    assert client is not None

def test_health_endpoint(client):
    """[AC] Accessing the '/health' endpoint returns a 200 OK status."""
    response = client.get("/health")
    assert response.status_code == 200

def test_database_connection():
    """[AC] The application successfully establishes and verifies a connection to the configured PostgreSQL database."""
    try:
        connection = engine.connect()
        connection.close()
    except OperationalError as e:
        pytest.fail(f"Database connection failed post-startup: {e}")

def test_faqs_table_and_schema():
    """[AC] The 'faqs' table is present and its schema matches models.py."""
    inspector = inspect(engine)
    assert "faqs" in inspector.get_table_names(), "Table 'faqs' should be created."

    columns = {c["name"] for c in inspector.get_columns("faqs")}
    expected_columns = {"id", "question", "answer", "category"}
    assert columns == expected_columns, "Schema of 'faqs' table is incorrect."
    
    # Deeper schema check
    cols_meta = inspector.get_columns("faqs")
    cols_map = {c['name']: c for c in cols_meta}
    assert isinstance(cols_map['id']['type'], sqlalchemy.types.Integer)
    assert cols_map['id']['primary_key'] == 1
    assert isinstance(cols_map['question']['type'], sqlalchemy.types.String)
    assert isinstance(cols_map['answer']['type'], sqlalchemy.types.Text)
    assert isinstance(cols_map['category']['type'], sqlalchemy.types.String)

def test_no_sensitive_data_logged_by_default(client, caplog):
    """[AC] Review of application logs confirms that no sensitive data is logged during normal operation."""
    # FastAPI and Uvicorn do not log request/response bodies by default.
    # This test verifies no 'sensitive' keyword appears in logs during a simple request.
    client.get("/health")
    for record in caplog.records:
        # A simple check for a word that might indicate sensitive data.
        assert "password" not in record.getMessage().lower()
        assert "token" not in record.getMessage().lower()
        assert "body" not in record.getMessage().lower()
