from behave import given, when, then
from tests.end_to_end_test.pages.login_page import LoginPage
import allure


@given(u'the application is running')
def step_impl(context):
    with allure.step("Verify application driver is available"):
        assert context.driver is not None


@given(u'the test database is already seeded with users')
def step_impl(context):
    with allure.step("Verify test database connection is available"):
        assert context.db is not None


@given(u'the employee is on the login screen')
def step_impl(context):
    with allure.step("Open the login page"):
        context.login_page = LoginPage(context.driver)
        context.login_page.open()


@when(u'the employee enters username "{username}"')
def step_impl(context, username):
    with allure.step(f'Enter username: "{username}"'):
        context.login_page.enter_username(username)


@when(u'the employee enters password "{password}"')
def step_impl(context, password):
    with allure.step(f'Enter password: "{password}"'):
        context.login_page.enter_password(password)


@when(u'the employee clicks the login button')
def step_impl(context):
    with allure.step("Click the login button"):
        context.dashboard_page = context.login_page.click_login_button()


@then(u'the employee sees the auth message: "{flash_message}"')
def step_impl(context, flash_message):
    with allure.step(f'Check auth flash message contains: "{flash_message}"'):
        message = context.login_page.wait_for_element(
            context.login_page.LOGIN_MESSAGE
        ).text

        assert flash_message in message


@then(u'the employee is redirected to the employee dashboard')
def step_impl(context):
    with allure.step('Verify the user is redirected to the employee dashboard (/app)'):
        context.dashboard_page.wait_for_url_contains("/app")
        assert "/app" in context.login_page.get_current_url()

@then(u'the employee is not redirected to the dashboard')
def step_impl(context):
    with allure.step('Verify the user is NOT redirected to the dashboard'):
        assert "/app" not in context.login_page.get_current_url()

@when(u'the employee does not input any value for username')
def step_impl(context):
    with allure.step('Clear the username input field'):
        username_input = context.login_page.wait_for_element(
            context.login_page.USERNAME_FIELD
        )
        username_input.clear()


@then(u'the username field is selected')
def step_impl(context):
    with allure.step('Assert the username field has focus'):
        active_element = context.driver.switch_to.active_element

        username_input = context.login_page.wait_for_element(
            context.login_page.USERNAME_FIELD
        )

        assert active_element == username_input


@given(u'the employee enters username "{username}"')
def step_impl(context, username):
    with allure.step(f'Enter username (given): "{username}"'):
        context.login_page.enter_username(username)


@when(u'the employee does not input any value for the password')
def step_impl(context):
    with allure.step('Clear the password input field'):
        password_input = context.login_page.wait_for_element(
            context.login_page.PASSWORD_FIELD
        )
        password_input.clear()


@then(u'the password field is selected')
def step_impl(context):
    with allure.step('Assert the password field has focus'):
        active_element = context.driver.switch_to.active_element

        password_input = context.login_page.wait_for_element(
            context.login_page.PASSWORD_FIELD
        )

        assert active_element == password_input


@given(u'the employee is logged in')
def step_impl(context):
    with allure.step('Ensure the employee is logged in (setup)'):
        context.login_page = LoginPage(context.driver)
        context.login_page.open()

        with allure.step('Enter credentials for employee1'):
            context.login_page.enter_username("employee1")
            context.login_page.enter_password("password123")

        with allure.step('Click login and wait for dashboard table'):
            context.dashboard_page = context.login_page.click_login_button()
            # Waiting for this element was the only thing that stopped tests for being flakey.
            # Most likely due to the fact that button eventlisteners attached after fetch and dom is set up.
            # The button only does something after the page fetches all expenses. Otherwise, it is just html.
            context.dashboard_page.wait_for_element(
                context.dashboard_page.TABLE
            )

        assert "/app" in context.login_page.get_current_url()


@when(u'the employee clicks the logout button')
def step_impl(context):
    with allure.step('Click the logout button'):
        context.login_page = context.dashboard_page.click_logout_button()


@then(u'the employee is redirected to the login page')
def step_impl(context):
    with allure.step('Verify user is redirected to the login page (/login)'):
        context.login_page.wait_for_url_contains("/login")
        assert "/login" in context.login_page.get_current_url()

