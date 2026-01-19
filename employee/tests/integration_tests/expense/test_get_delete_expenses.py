class TestDeleteExpenseAPI:
    def test_delete_expense_success(self, authenticated_session):
        """Test deleting a pending expense successfully."""
        # Expense 1 is pending for employee1
        expense_id = 1
        response = authenticated_session.delete(f"/api/expenses/{expense_id}")
        assert response.status_code == 200

        data = response.get_json()
        assert data["message"] == "Expense deleted successfully"

    def test_delete_expense_not_found(self, authenticated_session):
        """Test deleting a non-existent expense."""
        expense_id = 9999
        response = authenticated_session.delete(f"/api/expenses/{expense_id}")
        assert response.status_code == 404
        assert response.get_json()["error"] == "Expense not found"

    def test_delete_expense_isolation(self, authenticated_session):
        """Test that a user cannot delete another user's expense."""
        # Expense 4 belongs to employee2
        expense_id = 4
        response = authenticated_session.delete(f"/api/expenses/{expense_id}")
        assert response.status_code == 404
        assert response.get_json()["error"] == "Expense not found"

    def test_delete_expense_reviewed_fails(self, authenticated_session):
        """Test that approved or denied expenses cannot be deleted."""
        # Expense 2 is approved, Expense 3 is denied
        for expense_id in [2, 3]:
            response = authenticated_session.delete(f"/api/expenses/{expense_id}")
            # Actual error message: "Cannot delete expense that has been reviewed"
            assert response.status_code == 400
            assert "has been reviewed" in response.get_json()["error"].lower()

    def test_delete_expense_unauthorized(self, test_client):
        """Test deleting an expense without authentication."""
        expense_id = 1
        response = test_client.delete(f"/api/expenses/{expense_id}")
        assert response.status_code == 401
