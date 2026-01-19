import pytest
import allure


@allure.feature("Expense submission, editing, and deletion")
class TestSubmitExpenseAPI:
    @allure.story("Employee expense submission")
    @allure.title("Test api submit new expense success")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_api_submit_new_expense_success(self, authenticated_session):
        """Test submitting a valid expense."""
        payload = {
            "amount": 125.75,
            "description": "Taxi to client meeting",
            "date": "2025-01-10",
        }
        response = authenticated_session.post("/api/expenses", json=payload)
        assert response.status_code == 201

        data = response.get_json()
        assert data["message"] == "Expense submitted successfully"
        expense = data["expense"]
        assert expense["amount"] == 125.75
        assert expense["description"] == payload["description"]
        assert expense["date"] == payload["date"]
        assert expense["status"] == "pending"
        assert "id" in expense

    @allure.story("Employee expense submission")
    @allure.title("Test api submit expense validation fails")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize(
        "payload, expected_error",
        [
            ({"description": "No amount"}, "Amount and description are required"),
            ({"amount": 100}, "Amount and description are required"),
            (
                {"amount": "invalid", "description": "Bad amount"},
                "Amount must be a valid number",
            ),
            ({}, "JSON data required"),
        ],
    )
    def test_api_submit_expense_validation_fails(
        self, authenticated_session, payload, expected_error
    ):
        """Test validation rules for expense submission."""
        response = authenticated_session.post("/api/expenses", json=payload)
        assert response.status_code == 400
        assert response.get_json()["error"] == expected_error

    @allure.story("Employee expense submission")
    @allure.title("Test api submit expense unauthorized")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_api_submit_expense_unauthorized(self, test_client):
        """Test submitting an expense without authentication."""
        payload = {"amount": 50.0, "description": "Unauthorized"}
        # Using test_client specifically to ensure no session exists
        response = test_client.post("/api/expenses", json=payload)
        assert response.status_code == 401
