import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, inspect
from sqlalchemy.sql.sqltypes import Integer, String, Text

from main import app
from database import SQLALCHEMY_DATABASE_URL

# This fixture will ensure the app is started and tables are created before tests run.
@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope="module")
def engine():
    e = create_engine(SQLALCHEMY_DATABASE_URL)
    yield e
    e.dispose()

@pytest.fixture(scope="module")
def inspector(engine):
    return inspect(engine)

def test_app_starts_successfully(test_client):
    """
    - [x] The FastAPI application starts successfully without any errors.
    """
    # If the fixture is created, the application has started.
    assert test_client is not None

def test_health_endpoint(test_client):
    """
    - [x] Accessing the '/health' endpoint via an HTTP GET request returns a 200 OK status.
    """
    response = test_client.get("/health")
    assert response.status_code == 200

def test_database_connection_is_successful(engine):
    """
    - [x] The application successfully establishes and verifies a connection to the configured PostgreSQL database.
    """
    try:
        connection = engine.connect()
        connection.close()
    except Exception as e:
        pytest.fail(f"Database connection failed: {e}")

def test_faqs_table_and_schema_are_correct(test_client, inspector):
    """
    - [x] The 'faqs' table is present in the connected PostgreSQL database and its schema (columns: id, question, answer, category) matches the definition in 'models.py'.
    """
    # test_client fixture is needed to ensure the startup event that creates the table has run.
    assert inspector.has_table("faqs")

    columns = inspector.get_columns("faqs")
    column_details = {c["name"]: c for c in columns}

    assert "id" in column_details
    assert isinstance(column_details["id"]["type"], Integer)
    pk_constraint = inspector.get_pk_constraint("faqs")
    assert pk_constraint["constrained_columns"] == ["id"]

    assert "question" in column_details
    assert isinstance(column_details["question"]["type"], String)

    assert "answer" in column_details
    assert isinstance(column_details["answer"]["type"], Text)

    assert "category" in column_details
    assert isinstance(column_details["category"]["type"], String)

    indexes = inspector.get_indexes("faqs")
    indexed_columns = {idx["column_names"][0] for idx in indexes}
    assert "id" in indexed_columns
    assert "question" in indexed_columns
    assert "category" in indexed_columns

# Regarding AC:
# - [ ] Review of application logs confirms that no sensitive data (e.g., request bodies, authentication tokens) is logged during normal operation.
# This is confirmed by manual code review of 'main.py' which shows no custom logging configuration is added,
# thus relying on FastAPI's default which does not log sensitive information. An automated test for this
# is not straightforward with the current setup.
