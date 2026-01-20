from behave.api.pending_step import StepNotImplementedError
from behave import given, when, then
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@when('the employee clicks the edit button for the expense with description "{desc}"')

@when('the employee clicks the edit button for the expense with description "{desc}"')
def click_edit_button(context, desc):
    #  get the row with specified fields
    rows = context.driver.find_elements(By.TAG_NAME, "tr")
    specific_row = None
    for row in rows[1:]:
        row_description = row.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text
        if row_description == desc:
            specific_row = row
            break
    editButton = specific_row.find_element(
        By.CSS_SELECTOR, "button[onclick='expenseManager.editExpense(1)']"
    )
    editButton = specific_row.find_element(
        By.CSS_SELECTOR, "button[onclick='expenseManager.editExpense(1)']"
    )
    editButton.click()


@when("the employee is redirected to the edit menu")

@when("the employee is redirected to the edit menu")
def redirected_to_edit_menu(context):
    # header_locator = (By.CSS_SELECTOR, "div[id='edit-expense-section'] > h3")
    # header = context.dashboard_page.get_text(header_locator)
    # header = context.driver.find_element(By.CSS_SELECTOR, "#edit-expense-section > h3")
    # assert "Edit Expense" in header
    # header_locator = (By.CSS_SELECTOR, "div[id='edit-expense-section'] > h3")
    # header = context.dashboard_page.get_text(header_locator)
    # header = context.driver.find_element(By.CSS_SELECTOR, "#edit-expense-section > h3")
    # assert "Edit Expense" in header
    edit_amount_input_locator = (By.ID, "edit-amount")
    amount_field = context.dashboard_page.wait_for_clickable(edit_amount_input_locator)
    assert amount_field.is_displayed()


@when('the employee inputs into the amount field: "{amount}"')

@when('the employee inputs into the amount field: "{amount}"')
def input_amount(context, amount):
    amount_field_locator = (By.ID, "edit-amount")
    amount_field_locator = (By.ID, "edit-amount")
    context.dashboard_page.type(amount_field_locator, amount)


@when('the employee inputs into the description field: "{desc}"')

@when('the employee inputs into the description field: "{desc}"')
def input_description(context, desc):
    description_field_locator = (By.ID, "edit-description")
    context.dashboard_page.type(description_field_locator, desc)


@when('the employee inputs into the date field: "{date}"')

@when('the employee inputs into the date field: "{date}"')
def input_date(context, date):
    # adjust date format from YYYY-MM-DD to MM-DD-YYYY
    # adjust date format from YYYY-MM-DD to MM-DD-YYYY
    year = date[0:4]
    month = date[5:7]
    day = date[8:10]
    new_date = ""

    browser = context.driver.capabilities['browserName'].lower()

    if browser == "chrome":
        new_date = month + "/" + day + "/" + year
    else:
        new_date = date

    date_field_locator = (By.ID, "edit-date")
    context.dashboard_page.type(date_field_locator, new_date)


@when("the employee clicks the update expense button")

@when("the employee clicks the update expense button")
def click_update_expense_button(context):
    update_button_locator = (
        By.CSS_SELECTOR,
        "#edit-expense-form button[type='submit']",
    )
    update_button_locator = (
        By.CSS_SELECTOR,
        "#edit-expense-form button[type='submit']",
    )
    context.dashboard_page.click(update_button_locator)


@then('the employee sees the edit message: "{message}"')

@then('the employee sees the edit message: "{message}"')
def edit_message_shown(context, message):
    edit_message_locator = (By.CSS_SELECTOR, "#edit-message p")
    edit_message = context.dashboard_page.get_text(edit_message_locator)
    assert edit_message == message


@then('the expense is updated with the given "{amount}", "{desc}", and "{date}"')

@then('the expense is updated with the given "{amount}", "{desc}", and "{date}"')
def expense_is_shown_updated(context, amount, desc, date):
    # wait till you're back on the My Expenses screen
    # wait till you're back on the My Expenses screen
    refresh_button_locator = (By.ID, "refresh-expenses")
    refresh_button = context.dashboard_page.wait_for_clickable(refresh_button_locator)
    refresh_button.click()

    try:
        table_locator = (By.TAG_NAME, "table")
        old_table = context.dashboard_page.wait_for_element(table_locator)
        wait = WebDriverWait(context.driver, 5)
        wait.until(EC.staleness_of(old_table))
    except TimeoutException:
        # new table exists already
        pass

    # wait for all new elements to exist first
    context.dashboard_page.wait_for_element(
        (By.XPATH, f"//td[contains(text(), '${amount}')]")
    )
    context.dashboard_page.wait_for_element(
        (By.XPATH, f"//td[contains(text(), '{desc}')]")
    )
    context.dashboard_page.wait_for_element(
        (By.XPATH, f"//td[contains(text(), '{date}')]")
    )
    context.dashboard_page.wait_for_element(
        (By.XPATH, f"//td[contains(text(), 'PENDING')]")
    )
    # time.sleep(1)
    context.dashboard_page.wait_for_element(
        (By.XPATH, f"//td[contains(text(), '${amount}')]")
    )
    context.dashboard_page.wait_for_element(
        (By.XPATH, f"//td[contains(text(), '{desc}')]")
    )
    context.dashboard_page.wait_for_element(
        (By.XPATH, f"//td[contains(text(), '{date}')]")
    )
    context.dashboard_page.wait_for_element(
        (By.XPATH, f"//td[contains(text(), 'PENDING')]")
    )
    # time.sleep(1)
    # find the specific row with specified fields
    rows = context.driver.find_elements(By.TAG_NAME, "tr")
    found = False
    expected_amount = "$" + amount
    expected_amount = "$" + amount
    for row in rows[1:]:
        row_date = row.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text
        print(row_date + " vs " + date)
        print(row_date + " vs " + date)
        row_amount = row.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text
        print(row_amount + " vs " + expected_amount)
        print(row_amount + " vs " + expected_amount)
        row_description = row.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text
        print(row_description + " vs " + desc)
        print(row_description + " vs " + desc)
        row_status = row.find_element(By.CSS_SELECTOR, "td:nth-child(4)").text
        print(row_status + " vs PENDING")
        if (
            row_date == date
            and expected_amount in row_amount
            and row_description == desc
            and row_status == "PENDING"
        ):
            print(row_status + " vs PENDING")
        if (
            row_date == date
            and expected_amount in row_amount
            and row_description == desc
            and row_status == "PENDING"
        ):
            found = True
            break
    assert found


@when("the employee clicks the cancel button")

@when("the employee clicks the cancel button")
def click_cancel_button(context):
    cancel_button_locator = (By.ID, "cancel-edit")
    context.dashboard_page.click(cancel_button_locator)


@then('the expense with description "{desc}" still exists')

@then('the expense with description "{desc}" still exists')
def expense_with_description_still_exists(context, desc):
    # wait till you're back on the My Expenses screen
    refresh_button_locator = (By.ID, "refresh-expenses")
    context.dashboard_page.wait_for_clickable(refresh_button_locator)
    # get the row with specified fields
    rows = context.driver.find_elements(By.TAG_NAME, "tr")
    found = False
    for row in rows[1:]:
        row_description = row.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text
        row_status = row.find_element(By.CSS_SELECTOR, "td:nth-child(4)").text
        if row_description == desc and row_status == "PENDING":
            found = True
            break
    assert found


@then(
    'the expense is shown with the the amount: "{amount}", description: "{desc}", and the date: "{date}"'
)
def expense_shown_with_updates(context, amount, desc, date):
    # wait till you're back on the My Expenses screen
    refresh_button_locator = (By.ID, "refresh-expenses")
    refresh_button = context.dashboard_page.wait_for_clickable(refresh_button_locator)
    refresh_button.click()
    # wait for all new elements to exist first
    try:
        table_locator = (By.TAG_NAME, "table")
        old_table = context.dashboard_page.wait_for_element(table_locator)
        wait = WebDriverWait(context.driver, 10)
        wait.until(EC.staleness_of(old_table))
    except:
        pass
    # context.dashboard_page.wait_for_element((By.XPATH, f"//td[contains(text(), '${amount}')]"))
    # context.dashboard_page.wait_for_element((By.XPATH, f"//td[contains(text(), '{desc}')]"))
    # context.dashboard_page.wait_for_element((By.XPATH, f"//td[contains(text(), '{date}')]"))
    # context.dashboard_page.wait_for_element((By.XPATH, f"//td[contains(text(), 'PENDING')]"))
    # time.sleep(1)


@given(
    'an expense with the description: "{desc}", amount: "{amount}", and date: "{date}"'
)

@given(
    'an expense with the description: "{desc}", amount: "{amount}", and date: "{date}"'
)
def expense_with_values_exists(context, desc, amount, date):
    # get the row with specified fields
    rows = context.driver.find_elements(By.TAG_NAME, "tr")
    found = False
    expected_amount = "$" + amount
    expected_amount = "$" + amount
    for row in rows[1:]:
        row_date = row.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text
        row_amount = row.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text
        row_description = row.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text
        row_status = row.find_element(By.CSS_SELECTOR, "td:nth-child(4)").text
        if (
            row_date == date
            and expected_amount in row_amount
            and row_description == desc
            and row_status == "PENDING"
        ):
            found = True
            break
    assert found


@then(
    'the expense is shown with the the amount: "{amount}", description: "{desc}", and the date: "{date}"'
)

@then(
    'the expense is shown with the the amount: "{amount}", description: "{desc}", and the date: "{date}"'
)
def expense_shown_with_updates(context, amount, desc, date):
    # wait till you're back on the My Expenses screen
    refresh_button_locator = (By.ID, "refresh-expenses")
    refresh_button = context.dashboard_page.wait_for_clickable(refresh_button_locator)
    refresh_button.click()
    # wait for all new elements to exist first
    try:
        table_locator = (By.TAG_NAME, "table")
        old_table = context.dashboard_page.wait_for_element(table_locator)
        wait = WebDriverWait(context.driver, 5)
        wait.until(EC.staleness_of(old_table))
    except TimeoutException:
        # new table exists already
        pass

    context.dashboard_page.wait_for_element(
        (By.XPATH, f"//td[contains(text(), '${amount}')]")
    )
    context.dashboard_page.wait_for_element(
        (By.XPATH, f"//td[contains(text(), '{desc}')]")
    )
    context.dashboard_page.wait_for_element(
        (By.XPATH, f"//td[contains(text(), '{date}')]")
    )
    context.dashboard_page.wait_for_element(
        (By.XPATH, f"//td[contains(text(), 'PENDING')]")
    )
    # time.sleep(1)
    context.dashboard_page.wait_for_element(
        (By.XPATH, f"//td[contains(text(), '${amount}')]")
    )
    context.dashboard_page.wait_for_element(
        (By.XPATH, f"//td[contains(text(), '{desc}')]")
    )
    context.dashboard_page.wait_for_element(
        (By.XPATH, f"//td[contains(text(), '{date}')]")
    )
    context.dashboard_page.wait_for_element(
        (By.XPATH, f"//td[contains(text(), 'PENDING')]")
    )
    # time.sleep(1)
    # get the row with specified fields
    rows = context.driver.find_elements(By.TAG_NAME, "tr")
    found = False
    expected_amount = "$" + amount
    for row in rows[1:]:
        row_date = row.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text
        row_amount = row.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text
        row_description = row.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text
        row_status = row.find_element(By.CSS_SELECTOR, "td:nth-child(4)").text
        if (
            row_date == date
            and expected_amount in row_amount
            and row_description == desc
            and row_status == "PENDING"
        ):
            found = True
            break
    assert found


# @given(u'an expense with the description: "{desc}" is shown')
# def expense_with_description_is_shown(context, desc):

# @given(u'an expense with the description: "{desc}" is shown')
# def expense_with_description_is_shown(context, desc):
#    # get the row with specified fields
#    rows = context.driver.find_elements(By.TAG_NAME, "tr")
#    specific_row = None
#    for row in rows[1:]:
#        row_description = row.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text
#        if row_description == desc:
#            specific_row = row
#            break
#    assert specific_row.is_displayed()

# @given(u'the expense with description "{desc}" is pending')
# def expense_with_description_is_pending(context, desc):
# @given(u'the expense with description "{desc}" is pending')
# def expense_with_description_is_pending(context, desc):
#    # get the row with specified fields
#    rows = context.driver.find_elements(By.TAG_NAME, "tr")
#    specific_row = None
#    for row in rows[1:]:
#        row_description = row.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text
#        row_status = row.find_element(By.CSS_SELECTOR, "td:nth-child(4)").text
#        if row_description == desc and row_status == "PENDING":
#            specific_row = row
#            break
#    assert specific_row.is_displayed()

