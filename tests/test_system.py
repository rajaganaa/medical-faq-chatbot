import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

# This URL is for testing purposes only.
os.environ["DATABASE_URL"] = "postgresql://test_user:test_password@test_db/test_db"

from main import app
from database import Base

@pytest.fixture(scope="session")
def engine():
    test_db_url = os.getenv("DATABASE_URL")
    _engine = create_engine(test_db_url)
    Base.metadata.drop_all(bind=_engine)
    Base.metadata.create_all(bind=_engine)
    yield _engine
    Base.metadata.drop_all(bind=_engine)

@pytest.fixture(scope="function")
def db_session(engine):
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = Session()
    yield session
    session.close()
    transaction.rollback()
    connection.close()

# The test client initialization implicitly tests app startup.
# If the app fails to start, TestClient will raise an exception.
client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200

def test_database_connection(db_session):
    assert db_session.is_active

def test_faqs_table_creation(engine):
    inspector = inspect(engine)
    assert "faqs" in inspector.get_table_names()
    columns = {col["name"] for col in inspector.get_columns("faqs")}
    expected_columns = {"id", "question", "answer", "category"}
    assert columns == expected_columns
