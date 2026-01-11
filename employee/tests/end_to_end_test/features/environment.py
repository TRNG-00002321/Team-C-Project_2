import os
import requests
import time
from dotenv import load_dotenv
from src.repository import DatabaseConnection
from tests.end_to_end_test.drivers.browser_manager import create_driver

SEED_SQL_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../sql/seed.sql")
)

#implement multi browser functionality?

def before_all(context):
    # Read DB path from environment
    load_dotenv(override=False)
    db_path = os.getenv("BEHAVE_TEST_DATABASE_PATH")
    if not db_path:
        raise RuntimeError(
            "DATABASE_PATH is not set. "
            "Start the server with DATABASE_PATH pointing to a test database."
        )

    if not os.path.exists(db_path):
        raise RuntimeError(f"Database file not found at {db_path}")

    # Use the SAME database as the running server
    context.db = DatabaseConnection(db_path)
    
    # Wait for application to be ready
    base_url = os.getenv("BASE_URL", "http://localhost:5000")
    
    print(f"Waiting for application at {base_url}...")
    max_retries = 30
    retry_delay = 1
    for _ in range(max_retries):
        try:
            response = requests.get(f"{base_url}/health")
            if response.status_code == 200:
                print("Application is ready!")
                break
        except requests.exceptions.RequestException:
            pass
        time.sleep(retry_delay)
    else:
        raise RuntimeError(f"Application not reachable at {base_url} after 30 seconds")


def after_all(context):
    pass

def before_scenario(context, scenario):
    # --- Reset & reseed database ---
    with context.db.get_connection() as conn:
        conn.execute("DELETE FROM approvals")
        conn.execute("DELETE FROM expenses")
        conn.execute("DELETE FROM users")

        with open(SEED_SQL_PATH, "r") as f:
            conn.executescript(f.read())

        conn.commit()

    # --- Browser setup ---
    browser_type = os.getenv("BROWSER_TYPE", "chrome").lower()
    headless = os.getenv("HEADLESS", "false").lower() == "true"

    context.driver = create_driver(browser_type, headless)
    context.driver.maximize_window()


def after_scenario(context, scenario):
    if hasattr(context, 'driver') and context.driver:
        context.driver.quit()
