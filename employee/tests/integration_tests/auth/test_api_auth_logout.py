import pytest


# EI-217
class TestLogout:
    logout_url = "/api/auth/logout"

    def test_api_logout_success(self, authenticated_session):
        """
        Authenticated user can log out successfully
        """
        response = authenticated_session.post(self.logout_url)

        assert response.status_code == 200

        # After logout, cookie should be removed or empty
        auth_response = authenticated_session.get("/api/auth/status")
        json_response = auth_response.get_json()
        assert json_response.get("authenticated") is False

    @pytest.mark.skip(reason="Known bug")
    def test_api_logout_unauthorized(self, setup_database, test_client):
        auth_response = test_client.post(
            self.logout_url, json={"username": "employee1", "password": "password123"}
        )
        assert auth_response.status_code == 401

    # EI-218
    def test_api_access_protected_endpoint_fails_after_logout(
        self, authenticated_session
    ):
        # Logout
        logout_response = authenticated_session.post(self.logout_url)
        assert logout_response.status_code == 200

        # Try accessing protected endpoint
        response = authenticated_session.get("/api/expenses")

        assert response.status_code in (401, 403)
