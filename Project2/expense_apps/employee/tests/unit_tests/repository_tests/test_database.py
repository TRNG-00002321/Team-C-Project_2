import sqlite3
from unittest.mock import patch, MagicMock

import allure

from src.repository import DatabaseConnection

@allure.feature("Database Connection")
class TestDatabase:

    @allure.story("Shared Database")
    @allure.title("Test database connection returns a connection")
    @allure.severity(allure.severity_level.BLOCKER)
    @patch("src.repository.database.sqlite3.connect")
    def test_get_connection_returns_connection(mock_sqlite_connect):
      connection_mock = MagicMock()
      mock_sqlite_connect.return_value = connection_mock

      conn = DatabaseConnection("test.db").get_connection()

      mock_sqlite_connect.assert_called_once_with("test.db")
      assert conn == connection_mock

    @allure.story("Shared Database")
    @allure.title("Test initialize database")
    @allure.severity(allure.severity_level.BLOCKER)
    @patch("src.repository.database.DatabaseConnection.get_connection")
    def test_initialize_database_commit_called(mock_get_connection):
      mock_connection = MagicMock(spec=sqlite3.Connection)
      mock_connection.execute = MagicMock()
      mock_connection.commit = MagicMock()

      mock_get_connection.return_value.__enter__.return_value = mock_connection

      DatabaseConnection("test.db").initialize_database()

      assert mock_connection.execute.call_count == 3
      assert mock_connection.commit.called