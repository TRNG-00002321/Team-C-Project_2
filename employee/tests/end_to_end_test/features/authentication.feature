@auth @e2e @employee
Feature: Employee Authentication
  As an employee
  I want to login with my credentials
  So that I can securely access my expense reports

  Background:
    Given the application is running
    And the test database is already seeded with users

  @login @parameterized @smoke
  Scenario Outline: Login attempts
    Given the employee is on the login screen
    When the employee enters username "<username>"
    And the employee enters password "<password>"
    And the employee clicks the login button
    Then the employee sees the auth message: "<message>"


  Examples:
      | username    | password             | message                                                     |
      | employee1   | password123          | Login successful! Redirecting to employee dashboard...      |
      | wronguser   | password123          | Invalid credentials                                         |
      | employee1   | wrongpassword        | Invalid credentials                                         |
      | wronguser   | wrongpassword        | Invalid credentials                                         |
      | manager1    | password123          | Login failed                                                |

  @validation @negative
  Scenario Outline: Empty field validation
    Given the employee is on the login screen
    When the employee enters username "<username>"
    And the employee enters password "<password>"
    And the employee clicks the login button
    Then the login <field> field is selected
    And the employee is not redirected to the dashboard

  Examples:
      | field    | username   | password    |
      | username | none       | password123 |
      | password | employee1  |      none   |
      | username |     none   |   none      |

  @logout @sanity
  Scenario: Logout
    Given the employee is logged in
    When the employee clicks the logout button
    Then the employee is redirected to the login page
