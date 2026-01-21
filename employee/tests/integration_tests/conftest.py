import os
from src.main import create_app
from src.repository import DatabaseConnection
import pytest
from dotenv import load_dotenv

# TEST_DB_PATH = os.path.abspath(
#     os.path.join(os.path.dirname(__file__), "../test_db/test_expense_manager.db")
# )
# SEED_SQL_PATH = os.path.abspath(
#     os.path.join(os.path.dirname(__file__), "../sql/seed.sql")
# )


@pytest.fixture(scope="session")
def test_db_path():
    load_dotenv()
    return os.getenv("TEST_DATABASE_PATH")


@pytest.fixture(scope="session")
def seed_sql_path():
    load_dotenv()
    return os.getenv("SEED_SQL_PATH")


@pytest.fixture(scope="function")
def test_client(test_db_path):
    # Ensure test DB directory exists
    os.makedirs(os.path.dirname(test_db_path), exist_ok=True)

    # Set DB path BEFORE app creation
    os.environ["TEST_MODE"] = "true"
    os.environ["TEST_DATABASE_PATH"] = test_db_path

    # Initialize schema once
    db = DatabaseConnection()
    db.initialize_database()

    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


@pytest.fixture(scope="function")
def setup_database(test_client, test_db_path, seed_sql_path):
    """
    Reset database state before each test and reseed.
    Depends on test_client to guarantee schema exists.
    """
    db = DatabaseConnection()

    with db.get_connection() as conn:
        conn.execute("DELETE FROM approvals")
        conn.execute("DELETE FROM expenses")
        conn.execute("DELETE FROM users")

        with open(seed_sql_path, "r") as f:
            conn.executescript(f.read())

        conn.commit()

    yield


@pytest.fixture(scope="function")
def authenticated_session(test_client, setup_database):
    """
    Logs in as employee1 and returns an authenticated session
    """
    login_payload = {"username": "employee1", "password": "password123"}

    response = test_client.post("/api/auth/login", json=login_payload)

    assert response.status_code == 200

    yield test_client
