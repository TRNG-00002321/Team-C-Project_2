import pytest
import allure


@allure.feature("Expense submission, editing, and deletion")
class TestUpdateExpenseAPI:
    @allure.story("Employee editing expenses")
    @allure.title("Test update expense success")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_expense_success(self, authenticated_session):
        """Test updating a pending expense successfully."""
        expense_id = 1
        payload = {
            "amount": 99.99,
            "description": "Updated lunch",
            "date": "2025-01-06",
        }
        response = authenticated_session.put(
            f"/api/expenses/{expense_id}", json=payload
        )
        assert response.status_code == 200

        data = response.get_json()
        assert data["message"] == "Expense updated successfully"
        assert data["expense"]["amount"] == 99.99
        assert data["expense"]["description"] == "Updated lunch"

    @allure.story("Employee editing expenses")
    @allure.title("Test update expense validation fails")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize(
        "payload, expected_error",
        [
            (
                {"description": "Updated", "date": "2025-01-06"},
                "Amount, description, and date are required",
            ),
            (
                {"amount": 99.99, "date": "2025-01-06"},
                "Amount, description, and date are required",
            ),
            (
                {"amount": 99.99, "description": "Updated"},
                "Amount, description, and date are required",
            ),
            (
                {"amount": "abc", "description": "Updated", "date": "2025-01-06"},
                "Amount must be a valid number",
            ),
            ({}, "JSON data required"),
        ],
    )
    def test_update_expense_validation_fails(
        self, authenticated_session, payload, expected_error
    ):
        """Test validation rules for updating an expense."""
        expense_id = 1
        response = authenticated_session.put(
            f"/api/expenses/{expense_id}", json=payload
        )
        assert response.status_code == 400
        assert response.get_json()["error"] == expected_error

    @allure.story("Employee editing expenses")
    @allure.title("Test update expense not found")
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_expense_not_found(self, authenticated_session):
        """Test updating a non-existent expense."""
        expense_id = 9999
        payload = {"amount": 50.0, "description": "Missing", "date": "2025-01-06"}
        response = authenticated_session.put(
            f"/api/expenses/{expense_id}", json=payload
        )
        assert response.status_code == 404
        assert response.get_json()["error"] == "Expense not found"

    @allure.story("Employee editing expenses")
    @allure.title("Test update expense isolation")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_expense_isolation(self, authenticated_session):
        """Test that a user cannot update another user's expense."""
        # Expense 4 belongs to employee2
        expense_id = 4
        payload = {"amount": 10.0, "description": "Hack", "date": "2025-01-06"}
        response = authenticated_session.put(
            f"/api/expenses/{expense_id}", json=payload
        )
        assert response.status_code == 404

    @allure.story("Employee editing expenses")
    @allure.title("Test update expense approved denied fails")
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_expense_approved_denied_fails(self, authenticated_session):
        """Test that an approved or denied expense cannot be edited."""
        # Expense 2 is approved, Expense 3 is denied (for employee1)
        for expense_id in [2, 3]:
            payload = {
                "amount": 10.0,
                "description": "Editing reviewed expense",
                "date": "2025-01-06",
            }
            response = authenticated_session.put(
                f"/api/expenses/{expense_id}", json=payload
            )
            # Service should reject this
            assert response.status_code == 400
            assert "has been reviewed" in response.get_json()["error"].lower()

    @allure.story("Employee editing expenses")
    @allure.title("Test update expense unauthorized")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_expense_unauthorized(self, test_client):
        """Test updating an expense without authentication."""
        expense_id = 1
        payload = {"amount": 10.0, "description": "Unauthorized", "date": "2025-01-06"}
        response = test_client.put(f"/api/expenses/{expense_id}", json=payload)
        assert response.status_code == 401
