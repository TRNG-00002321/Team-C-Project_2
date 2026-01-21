from behave import given, when, then
from selenium.webdriver.common.by import By
from datetime import datetime, date

from tests.end_to_end_test.pages.dashboard_page import DashboardPage



def get_dashboard_page(context):
    if not hasattr(context, 'dashboard_page'):
        context.dashboard_page=DashboardPage(context.driver)
    return context.dashboard_page

@given(u'the employee is at the submit expense menu')
def employee_at_submit_expense_page(context):
    context.dashboard_page = DashboardPage(context.driver)
    return context.dashboard_page.go_to_submit_new_expense_screen()


@when(u'the employee inputs a new amount: "{amount}"')
def step_enter_amount(context, amount):
    context.dashboard_page = DashboardPage(context.driver)
    amount_input = context.dashboard_page.wait_for_element((By.ID, 'amount'))
    amount_input.clear()
    # Treat the token EMPTY as "do not type anything" (leave blank)
    if amount != "EMPTY":
        amount_input.send_keys(amount)


@when(u'the employee inputs a new description: "{description}"')
def step_enter_description(context, description):
    context.dashboard_page = DashboardPage(context.driver)
    description_input = context.dashboard_page.wait_for_element((By.ID, 'description'))
    description_input.clear()
    # Treat the token EMPTY as "do not type anything" (leave blank)
    if description != "EMPTY":
        description_input.send_keys(description)


def _possible_display_dates_from_iso(iso_date_str):
    """
    Given an ISO date string YYYY-MM-DD, return a set of likely display formats
    that the UI might show (e.g., MM/DD/YYYY, DD/MM/YYYY, and the ISO itself).
    """
    try:
        y = int(iso_date_str[0:4])
        m = int(iso_date_str[5:7])
        d = int(iso_date_str[8:10])
    except Exception:
        return {iso_date_str}

    mm = f"{m:02d}"
    dd = f"{d:02d}"
    yyyy = f"{y:04d}"

    formats = set()
    formats.add(iso_date_str)
    formats.add(f"{mm}/{dd}/{yyyy}")
    formats.add(f"{dd}/{mm}/{yyyy}")
    # also add non-zero-padded variants just in case
    formats.add(f"{m}/{d}/{yyyy}")
    formats.add(f"{d}/{m}/{yyyy}")
    return formats


@when(u'the employee inputs a new date: "{date_val}"')
def step_enter_date(context, date_val):
    context.dashboard_page = DashboardPage(context.driver)

    # Tokens handling
    if date_val == "EMPTY":
        # clear and leave the date blank
        date_field_locator = (By.ID, "date")
        date_input = context.dashboard_page.wait_for_element(date_field_locator)
        date_input.clear()
        return

    if date_val == "TODAY":
        date_val = date.today().strftime("%Y-%m-%d")

    # Expecting date_val in ISO format YYYY-MM-DD here
    if len(date_val) >= 10:
        year = date_val[0:4]
        month = date_val[5:7]
        day = date_val[8:10]
    else:
        # fallback: try to parse loosely
        parsed = datetime.strptime(date_val, "%Y-%m-%d")
        year = parsed.strftime("%Y")
        month = parsed.strftime("%m")
        day = parsed.strftime("%d")

    new_date = ""
    browser = context.driver.capabilities.get('browserName', '').lower()

    if browser == "chrome":
        new_date = month + "/" + day + "/" + year
    elif browser == "edge":
        new_date = day + "/" + month + "/" + year
    else:
        new_date = date_val


    date_field_locator = (By.ID, "date")
    context.dashboard_page.type(date_field_locator, new_date)


@when(u'the employee clicks the submit expense button')
def step_click_submit_expense_button(context):
    context.dashboard_page = DashboardPage(context.driver)
    click_button = context.dashboard_page.wait_for_clickable((By.XPATH, "//button[@type='submit']"))
    click_button.click()


@then(u'the employee sees the message: "{text}"')
def step_successful_expense_submission(context, text):
    context.dashboard_page = DashboardPage(context.driver)
    message = context.dashboard_page.get_text((By.CSS_SELECTOR, '#submit-message > p'))
    assert text in message, f"Expected {text} in {message}"


@then(u'the employee navigates to the expenses screen')
def step_go_to_expenses(context):
    context.dashboard_page = DashboardPage(context.driver)
    return context.dashboard_page.go_to_view_my_expenses_screen()


@then(u'the expense is shown with the amount: "{amount}", description: "{description}", and the date: "{expected_date}"')
def step_expense_is_shown(context, amount, description, expected_date):
     context.dashboard_page = DashboardPage(context.driver)

     # Convert expected_date token TODAY -> actual iso string
     if expected_date == "TODAY":
         expected_iso = date.today().strftime("%Y-%m-%d")
     else:
         expected_iso = expected_date

     possible_dates = _possible_display_dates_from_iso(expected_iso)

     # Wait until at least the amount and description are present in the table somewhere
     # (This is a loose wait to let the table render)
     context.dashboard_page.wait_for_element((By.XPATH, f"//td[contains(text(), '${amount}')]"))
     context.dashboard_page.wait_for_element((By.XPATH, f"//td[contains(text(), '{description}')]"))

     rows = context.driver.find_elements(By.TAG_NAME, "tr")
     found = False
     expected_amount = "$" + amount
     for row in rows[1:]:
         try:
             row_date = row.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text
             row_amount = row.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text
             row_description = row.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text
         except Exception:
             continue

         # Accept different date display formats by checking containment
         date_matches = any(p in row_date for p in possible_dates)
         amount_matches = expected_amount in row_amount
         description_matches = row_description == description

         if date_matches and amount_matches and description_matches:
             found = True
             break
     assert found, f"Expense not found: {amount}, {description}, {expected_iso}"


@when(u'the amount field is empty')
def step_empty_amount_field(context):
    #dashboard_page = DashboardPage(context.driver)
    context.dashboard_page = DashboardPage(context.driver)
    amount_field = context.dashboard_page.wait_for_element((By.ID, 'amount'))
    value = amount_field.get_attribute("value")
    assert value == "", f"Expected amount field is to be empty, but found '{value}'"


@then(u'the amount field is selected')
def step_empty_field_prompts_for_amount(context):
    #dashboard_page = DashboardPage(context.driver)
    context.dashboard_page = DashboardPage(context.driver)
    amount_field = context.dashboard_page.wait_for_element((By.ID, 'amount'))
    is_focused = amount_field == context.driver.switch_to.active_element
    assert is_focused, "Amount field is not selected or focused as expected"


@then(u'the employee stays on the submit menu screen')
def step_user_remains_on_submit_menu(context):
    #dashboard_page = DashboardPage(context.driver)
    context.dashboard_page = DashboardPage(context.driver)
    stay_on_page = context.dashboard_page.is_displayed((By.ID, 'submit-expense-section'))
    assert stay_on_page, "Employee is not on the submit menu"


@when(u'the description field is empty')
def step_empty_description_field(context):
    #dashboard_page = DashboardPage(context.driver)
    context.dashboard_page = DashboardPage(context.driver)
    description_field = context.dashboard_page.wait_for_element((By.ID, 'description'))
    value = description_field.get_attribute("value")
    assert value == "", f"Expected description field is to be empty, but found '{value}'"


@then(u'the description field is selected')
def step_empty_field_prompts_for_description(context):
    #dashboard_page = DashboardPage(context.driver)
    context.dashboard_page = DashboardPage(context.driver)
    description_field = context.dashboard_page.wait_for_element((By.ID, 'description'))
    is_focused = description_field == context.driver.switch_to.active_element
    assert is_focused, "Description field is not selected or focused as expected"


@then(u'an expense with today\'s date, amount: "{amount}" and description: "{description}" is shown')
def step_automatic_date_inception(context, amount, description):
    #dashboard_page = DashboardPage(context.driver)
    context.dashboard_page = DashboardPage(context.driver)

    context.dashboard_page.wait_for_element((By.XPATH, f"//td[contains(text(), '${amount}')]"))
    context.dashboard_page.wait_for_element((By.XPATH, f"//td[contains(text(), '{description}')]"))
    expected_date = date.today().strftime("%Y-%m-%d")

    rows = context.driver.find_elements(By.TAG_NAME, "tr")
    found = False
    expected_amount = "$" + amount
    for row in rows[1:]:
        row_date = row.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text
        print(row_date)
        row_amount = row.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text
        print(row_amount)
        row_description = row.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text
        print(row_description)
        if expected_date in row_date and expected_amount in row_amount and row_description == description:
            found = True
            break
    assert found, f"Expense not found: {amount}, {description}, {expected_date}"


@then(u'the "{focus_field}" field is selected')
def step_focus_field_selected(context, focus_field):
    """Generic step to handle generated steps like: Then the "amount" field is selected
    Delegates to the existing specific step implementations for amount/description.
    """
    focus_field_lower = focus_field.lower()
    if focus_field_lower == 'amount':
        return step_empty_field_prompts_for_amount(context)
    if focus_field_lower == 'description':
        return step_empty_field_prompts_for_description(context)

