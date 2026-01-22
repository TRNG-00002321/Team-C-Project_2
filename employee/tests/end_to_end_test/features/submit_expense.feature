Feature: Submit new expense
  As an employee
  I want to submit new expenses with details about amount and description
  So that I can request reimbursement or track spending

Background:
  Given the application is running
  And the test database is already seeded with users
  And the employee is logged in

Scenario Outline: Successful expense submit
  Given the employee is at the submit expense menu
  When the employee inputs a new amount: "<amount>"
  And the employee inputs a new description: "<description>"
  And the employee inputs a new date: "<date>"
  And the employee clicks the submit expense button
  Then the employee sees the message: "Expense submitted successfully!"
  And the employee navigates to the expenses screen
  And the expense is shown with the amount: "<amount>", description: "<description>", and the date: "<expected_date>"

  Examples: Successful submissions
      | amount | description         | date       | expected_date |
      | 123    | example description | 2025-12-31 | 2025-12-31    |
      | 999    | fix door            | 2025-01-01 | 2025-01-01    |
      | 100    | todays date         | TODAY      | TODAY         |

  @validation
  Scenario Outline: Submit expense validation (empty required fields)
    Given the employee is at the submit expense menu
    When the employee inputs a new amount: "<amount>"
    And the employee inputs a new description: "<description>"
    And the employee clicks the submit expense button
    Then the "<focus_field>" field is selected
    And the employee stays on the submit menu screen

    Examples: Validation errors
      | amount | description | focus_field |
      | EMPTY  | example     | amount      |
      | 125    | EMPTY       | description |
