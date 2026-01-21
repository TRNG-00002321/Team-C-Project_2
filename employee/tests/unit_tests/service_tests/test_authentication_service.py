from unittest.mock import MagicMock, patch

import allure
import jwt
import pytest

from src.repository import UserRepository, User
from src.service import AuthenticationService

@allure.feature("Employe authorization")
class Test_Authentication_Service:

    @pytest.fixture
    def setup(self):
        mock_repo = MagicMock(spec=UserRepository)
        service = AuthenticationService(mock_repo, "secretKey")
        return mock_repo, service

    @allure.story("Employee login")
    @allure.title("Test authenticate user")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("repo_user, username, password, expectedResult", [
        # EU-011
        (User(1, "testUser1", "testPassword1", "Employee"), "testUser1", "testPassword1", User(1, "testUser1", "testPassword1", "Employee")),
        # EU-012
        (User(1, "testUser1", "testPassword1", "Employee"), "testUser1", "testPassword2", None),
        # EU-013
        (None, "missing", "missing", None)
    ])
    def test_authenticate_user(self, setup, repo_user, username, password, expectedResult):
        # Assign
        setup[0].find_by_username.return_value = repo_user
        # Act
        result = setup[1].authenticate_user(username, password)
        # Assign
        assert result == expectedResult
        setup[0].find_by_username.assert_called_once_with(username)

    @allure.story("Employee login")
    @allure.title("Test get user by id")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("user_id, repo_result, expected", [
        # EU-014
        (1, User(1, "testUser1", "pass", "Employee"), User(1, "testUser1", "pass", "Employee")),
        # EU-015
        (2, None, None),
    ])
    def test_get_user_by_id(self, setup, user_id, repo_result, expected):
        # Assign
        setup[0].find_by_id.return_value = repo_result

        # Act
        result = setup[1].get_user_by_id(user_id)

        # Assert
        assert result == expected
        setup[0].find_by_id.assert_called_once_with(user_id)

    # EU-016
    @allure.story("Employee login")
    @allure.title("Test generate jwt token")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_generate_jwt_token(self, setup):
        # Assign
        user = User(1, "testUser", "pass", "Employee")

        # Act
        with patch("jwt.encode", return_value="encoded.jwt") as mock_encode:
            token = setup[1].generate_jwt_token(user)

        # Assert
        assert token == "encoded.jwt"
        mock_encode.assert_called_once()

    # EU-017
    @allure.story("Employee login")
    @allure.title("Test validate jwt token, valid")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_validate_jwt_token_valid(self, setup):
        # Assign
        token = "valid.token"
        payload = {"user_id": 123}

        # Act
        with patch("jwt.decode", return_value=payload):
            result = setup[1].validate_jwt_token(token)

        # Assert
        assert result == payload

    # EU-018, EU-019
    @allure.story("Employee login")
    @allure.title("Test validate jwt token, invalid")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize(
        "exception",
        [jwt.ExpiredSignatureError, jwt.InvalidTokenError],
    )
    def test_validate_jwt_token_invalid(self, setup, exception):
        # Act
        with patch("jwt.decode", side_effect=exception):
            result = setup[1].validate_jwt_token("bad.token")

        # Assert
        assert result is None

    # EU-20
    @allure.story("Employee login")
    @allure.title("Test get user from jwt token, valid")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_user_from_token_valid(self, setup):
        # Assign
        token = "valid.token"
        payload = {"user_id": 1}
        user1 = User(1, "testUser1", "testPassword1", "Employee")

        # Act
        with patch.object(setup[1],"validate_jwt_token", return_value=payload), \
            patch.object(setup[1], "get_user_by_id", return_value=user1):
            result = setup[1].get_user_from_token(token)

        # Assert
        assert result == user1

    # EU-21
    @allure.story("Employee login")
    @allure.title("Test get user from jwt token, invalid")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_user_from_token_invalid(self, setup):
        # Assign
        token = "invalid.token"
        payload = None

        # Act
        with patch.object(setup[1], "validate_jwt_token", return_value=payload):
            result = setup[1].get_user_from_token(token)

        # Assert
        assert result is None