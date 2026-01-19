import pytest
import allure


@allure.feature("Employee authorization")
class TestLoginAPI:
    @allure.story("Employee login")
    @allure.title("Test login positive")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_positive(self, test_client, setup_database):
        data = {"username": "employee1", "password": "password123"}
        response = test_client.post("/api/auth/login", json=data)
        assert response.status_code == 200
        user = response.get_json()["user"]
        assert user["username"] == "employee1"
        assert user["role"] == "Employee"
        assert user["id"] == 1

    @allure.story("Employee login")
    @allure.title("Test login invalid credentials")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize(
        "username, password",
        [
            ("employee1", "wrong_password"),
            ("wrong_username", "password123"),
            (12345, 12345),
        ],
    )
    def test_login_invalid_credentials(
        self, username, password, test_client, setup_database
    ):
        data = {"username": username, "password": password}
        response = test_client.post("/api/auth/login", json=data)
        assert response.status_code == 401

    @allure.story("Employee login")
    @allure.title("Test login invalid data")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize(
        "username, password",
        [
            ("", ""),
            (None, None),
        ],
    )
    def test_login_invalid_data(self, username, password, test_client, setup_database):
        data = {"username": username, "password": password}

        response = test_client.post("/api/auth/login", json=data)
        assert response.status_code == 400
        assert "Username and password required" in response.get_json()["error"]
