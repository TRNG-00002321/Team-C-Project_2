import pytest
import allure


@allure.feature("Expense submission, editing, and deletion")
class TestSpecificExpenseAPI:
    @allure.story("Employee viewing expenses")
    @allure.title("Test get specific expense by id positive")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize(
        "expense_id, expected_amount", [(1, 50.0), (2, 200.0), (3, 30.0), (6, 200.0)]
    )
    def test_get_specific_expense_by_id_positive(
        self, authenticated_session, expense_id, expected_amount
    ):
        """Test retrieving specific expenses belonging to the authenticated user."""
        response = authenticated_session.get(f"/api/expenses/{expense_id}")
        assert response.status_code == 200

        data = response.get_json()
        assert "expense" in data
        expense_data = data["expense"]

        assert expense_data["id"] == expense_id
        assert expense_data["amount"] == expected_amount
        assert isinstance(expense_data["amount"], (int, float))
        assert "status" in expense_data
        assert "description" in expense_data

    @allure.story("Employee viewing expenses")
    @allure.title("Test get specific expense by id not found")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("expense_id", [999, 0])
    def test_get_specific_expense_by_id_not_found(
        self, authenticated_session, expense_id
    ):
        """Test retrieving non-existent expense IDs (within integer range)."""
        response = authenticated_session.get(f"/api/expenses/{expense_id}")
        assert response.status_code == 404
        assert response.get_json()["error"] == "Expense not found"

    @allure.story("Employee viewing expenses")
    @allure.title("Test get specific expense by id isolation")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("expense_id", [4, 5])
    def test_get_specific_expense_by_id_isolation(
        self, authenticated_session, expense_id
    ):
        """Test that a user cannot access another user's expense."""
        # IDs 4 and 5 belong to employee2 (user_id 2). authenticated_session is employee1.
        response = authenticated_session.get(f"/api/expenses/{expense_id}")
        assert response.status_code == 404
        assert response.get_json()["error"] == "Expense not found"

    @allure.story("Employee viewing expenses")
    @allure.title("Test get specific expense by id invalid format")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.parametrize("expense_id", ["abc", "1.5", "@#$", -1])
    def test_get_specific_expense_by_id_invalid_format(
        self, authenticated_session, expense_id
    ):
        """Test retrieving expenses with invalid ID formats or out-of-range values."""
        response = authenticated_session.get(f"/api/expenses/{expense_id}")
        # Flask routing <int:expense_id> returns 404 for non-positive integers
        assert response.status_code == 404

    @allure.story("Employee viewing expenses")
    @allure.title("Test get specific expense unauthorized")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_expense_unauthorized(self, test_client):
        """Test retrieving an expense without authentication."""
        response = test_client.get("/api/expenses/1")
        assert response.status_code == 401
