class TestAuthenticationAPI:
    status_url = "/api/auth/status"

    # Status tests
    def test_status_unauthenticated(self, test_client, setup_database):
        response = test_client.get(self.status_url)
        assert response.status_code == 200
        json_response = response.get_json()
        assert json_response.get("authenticated") is False

    def test_status_authenticated_valid_cred(self, authenticated_session):
        status_response = authenticated_session.get(self.status_url)
        assert status_response.status_code == 200
        data = status_response.get_json()
        assert data["authenticated"] is True

    def test_status_invalid_cred(self, test_client, setup_database):
        test_client.post(
            "/api/auth/login",
            json={"username": "manager1", "password": "password123", "role": "manager"},
        )
        response = test_client.get(self.status_url)
        assert response.status_code == 200
        json_response = response.get_json()
        assert json_response.get("authenticated") is False
