import pytest
import allure


@allure.feature("Expense submission, editing, and deletion")
class TestAllExpenseAPI:
    @allure.story("Employee viewing expenses")
    @allure.title("Test get all expense positive")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_all_expense_positive(self, authenticated_session):
        """Test retrieving all expenses for personal user."""
        response = authenticated_session.get("/api/expenses")
        assert response.status_code == 200

        data = response.get_json()
        assert "expenses" in data
        assert "count" in data
        assert isinstance(data["expenses"], list)
        # employee1 has 4 expenses in seed.sql (IDs 1, 2, 3, 6)
        assert data["count"] == 4

    @allure.story("Employee viewing expenses")
    @allure.title("Test get expenses with status filter")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize(
        "status_filter, expected_count",
        [
            ("pending", 2),  # IDs 1, 6
            ("approved", 1),  # ID 2
            ("denied", 1),  # ID 3
            ("invalid", 4),  # Service ignores invalid filters and returns all
        ],
    )
    def test_get_expenses_with_status_filter(
        self, authenticated_session, status_filter, expected_count
    ):
        """Test filtering expenses by status."""
        response = authenticated_session.get(f"/api/expenses?status={status_filter}")
        assert response.status_code == 200
        data = response.get_json()
        assert data["count"] == expected_count

    @allure.story("Employee viewing expenses")
    @allure.title("Test get all expense unauthorized")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_all_expense_unauthorized(self, test_client):
        """Test retrieving expenses without authentication."""
        # Using test_client specifically to ensure no session exists
        response = test_client.get("/api/expenses")
        assert response.status_code == 401
