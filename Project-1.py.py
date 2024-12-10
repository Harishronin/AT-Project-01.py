
"""
Test case ID:TC_login_01

Test objective:
  Successful employee login to OrangeHRM Portal
Precondition:
 1.A valid ESS-User Account to login to be available
2.A orangeHRM 3.0 site is launche on compatible browser

Steps:
 1.In the login panel,enter the user name(Test data: “Admin”)
2.Enter the password for ESS User account in the password field (Test data:”admin123”)
3.Click”login”button

 Expected result:
The user is logged successfully
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Test case ID and objective
test_case_id = "TC_login_01"
test_objective = "Successful employee login to OrangeHRM Portal"

# Initialize the WebDriver
driver = webdriver.Chrome()  

try:
    # Launch the OrangeHRM site
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    driver.maximize_window()

    # Wait object
    wait = WebDriverWait(driver, 10)

    # Step 1: Enter the username
    username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    username_field.clear()  # Clear any pre-filled data
    username_field.send_keys("Admin")

    # Step 2: Enter the password
    password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    password_field.clear()
    password_field.send_keys("admin123")

    # Step 3: Click the login button
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
    login_button.click()

    # Step 4: Verify if the login was successful
    dashboard_header = wait.until(EC.presence_of_element_located((By.XPATH, "//h6[text()='Dashboard']")))

    # If the Dashboard is visible, the login is successful
    if dashboard_header.is_displayed():
        print(f"{test_case_id}: {test_objective} - Passed")
    else:
        print(f"{test_case_id}: {test_objective} - Failed: Dashboard not visible")

except Exception as e:
    # Capture and display any errors
    print(f"{test_case_id}: {test_objective} - Failed. Error: {str(e)}")
finally:
    # Close the browser
    driver.quit()


"""
Test case ID:TC_login_02

Test objective:
Invalid employee login to orangeHRM portal

Precondition:
 1.A valid ESS-User Account to login to be available
2.A orangeHRM 3.0 site is launche on compatible browser

Steps:
 1.In the login panel,enter the user name(Test data: “Admin”)
2.Enter the password for ESS User account in the password field (Test data:”admin123”)
3.Click”login”button

 Expected result:
A valid error message displayed for invalid credentials is displayed.

TestCases dealing with the PIM:
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Define test case ID and objective
test_case_id = "TC_login_02"
test_objective = "Invalid employee login to OrangeHRM portal"

# Initialize the WebDriver
driver = webdriver.Chrome()  

try:
    # Step 1: Launch the OrangeHRM site and maximize the window
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    driver.maximize_window()

    # Initialize explicit wait
    wait = WebDriverWait(driver, 10)

    # Step 2: Enter the username
    username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    username_field.clear()
    username_field.send_keys("Admin")

    # Step 3: Enter an incorrect password
    password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    password_field.clear()
    password_field.send_keys("wrongpassword")

    # Step 4: Click the login button
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
    login_button.click()

    # Step 5: Verify the error message is displayed
    error_message = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//p[@class='oxd-text oxd-text--p oxd-alert-content-text']"))
    )

    # Step 6: Assert the error message matches the expected text
    assert "Invalid credentials" in error_message.text, "Error message does not match expected text"

    # Test passed
    print(f"{test_case_id}: {test_objective} - Passed")

except AssertionError as ae:
    # Handle assertion errors separately
    print(f"{test_case_id}: {test_objective} - Failed. Assertion Error: {str(ae)}")
except Exception as e:
    # Handle any other exceptions
    print(f"{test_case_id}: {test_objective} - Failed. Error: {str(e)}")
finally:
    # Close the browser
    driver.quit()




"""
Test case ID:TC_PIM_01

Test objective:
Add a new employee in the PIM Module

Precondition:
 1.A valid ESS-User Account to login to be available
2.A orangeHRM 3.0 site is launche on compatible browser
Steps:
1.Go to PIM Module from the left pane in the web page.
2.Click on Add and add new employee details in the page
3.Fill in all the personal details of the employee and click save

Expected Result:
The user should be able to add new employee in the PIM and should see a message successful employee addition.

"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    """Page Object Model for OrangeHRM Login Page."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.username_field = (By.NAME, "username")
        self.password_field = (By.NAME, "password")
        self.login_button = (By.XPATH, "//button[@type='submit']")
        self.pim_module_link = (By.XPATH, "//a[@href='/web/index.php/pim/viewPimModule']")

    def open(self, url):
        """Opens the login page."""
        self.driver.get(url)

    def login(self, username, password):
        """Logs in to the application."""
        self.wait.until(EC.presence_of_element_located(self.username_field)).send_keys(username)
        self.wait.until(EC.presence_of_element_located(self.password_field)).send_keys(password)
        self.driver.find_element(*self.password_field).send_keys(Keys.RETURN)

    def is_pim_module_visible(self):
        """Checks if the PIM module is visible after login."""
        return self.wait.until(EC.presence_of_element_located(self.pim_module_link)).is_displayed()

import pytest
from selenium import webdriver


@pytest.fixture(scope="function")
def driver():
    """Initializes the WebDriver."""
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

import pytest
from pages.login_page import LoginPage
from pages.pim_page import PIMPage


def test_add_employee(driver):
    """
    Test Case: Add a new employee to the PIM module
    """
    # Test data
    url = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
    username = "Admin"
    password = "admin123"
    first_name = "John"
    middle_name = "A"
    last_name = "Doe"

    # Initialize Page Objects
    login_page = LoginPage(driver)
    pim_page = PIMPage(driver)

    # Step 1: Open the login page
    login_page.open(url)

    # Step 2: Log in
    login_page.login(username, password)
    assert login_page.is_pim_module_visible(), "Login failed or PIM module not visible"

    # Step 3: Navigate to PIM module
    driver.find_element(By.XPATH, "//a[@href='/web/index.php/pim/viewPimModule']").click()

    # Step 4: Add a new employee
    pim_page.navigate_to_add_employee()
    pim_page.add_employee(first_name, middle_name, last_name)

    # Step 5: Verify the employee was added successfully
    assert pim_page.is_success_message_visible(), "Employee addition failed"
    print("Test Passed: Employee was added successfully.")


"""
Test case ID:TC_PIM_02

Test objective:
Edit an existing employee in the PIM Module

Precondition:
 1.A valid ESS-User Account to login to be available
2.A orangeHRM 3.0 site is launche on compatible browser
Steps:
1.Go to PIM Module from the left pane in the web page.
2.From the existing list of Employees in the PIM Module.
edit the employee information of the employee and save it.

Expected Result:
The user should be able to edit an existing employee information in the PIM and should see a message successful employee details addition.


"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class PIMPage:
    """Page Object Model for the PIM Module."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.add_button = (By.XPATH, "//button[normalize-space()='Add']")
        self.first_name_field = (By.NAME, "firstName")
        self.middle_name_field = (By.NAME, "middleName")
        self.last_name_field = (By.NAME, "lastName")
        self.save_button = (By.XPATH, "//button[normalize-space()='Save']")
        self.success_message = (By.XPATH, "//div[contains(text(), 'Successfully')]")

    def navigate_to_add_employee(self):
        """Clicks the Add button to add a new employee."""
        self.wait.until(EC.element_to_be_clickable(self.add_button)).click()

    def add_employee(self, first_name, middle_name, last_name):
        """Fills in the employee details and clicks Save."""
        self.wait.until(EC.presence_of_element_located(self.first_name_field)).send_keys(first_name)
        self.driver.find_element(*self.middle_name_field).send_keys(middle_name)
        self.driver.find_element(*self.last_name_field).send_keys(last_name)
        self.driver.find_element(*self.save_button).click()

    def is_success_message_visible(self):
        """Checks if the success message is visible."""
        return self.wait.until(EC.presence_of_element_located(self.success_message)).is_displayed()

import pytest
from pages.login_page import LoginPage
from pages.pim_page import PIMPage


def test_add_employee(driver):
    """
    Test Case: Add a new employee to the PIM module
    """
    # Test data
    url = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
    username = "Admin"
    password = "admin123"
    first_name = "John"
    middle_name = "A"
    last_name = "Doe"

    # Initialize Page Objects
    login_page = LoginPage(driver)
    pim_page = PIMPage(driver)

    # Step 1: Open the login page
    login_page.open(url)

    # Step 2: Log in
    login_page.login(username, password)
    assert login_page.is_pim_module_visible(), "Login failed or PIM module not visible"

    # Step 3: Navigate to PIM module
    driver.find_element(By.XPATH, "//a[@href='/web/index.php/pim/viewPimModule']").click()

    # Step 4: Add a new employee
    pim_page.navigate_to_add_employee()
    pim_page.add_employee(first_name, middle_name, last_name)

    # Step 5: Verify the employee was added successfully
    assert pim_page.is_success_message_visible(), "Employee addition failed"
    print("Test Passed: Employee was added successfully.")


"""

Test case ID:TC_PIM_03

Test objective:
Delete an existing employee in the PIM Module

Precondition:
 1.A valid ESS-User Account to login to be available
2.A orangeHRM 3.0 site is launche on compatible browser

Steps:
1.Go to PIM Module from the left pane in the web page.
2.From the existing list of Employees in the PIM Module.delete an existing employee.

Expected Result:
The user should be able to delete an existing employee information in the PIM and should see a message successful deletion.


"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class PIMPage:
    """Page Object Model for the PIM Module."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.employee_card = (By.XPATH, "(//div[@class='oxd-table-card'])[1]")
        self.delete_button = (By.XPATH, "//button[normalize-space()='Delete']")
        self.confirm_delete_button = (By.XPATH, "//button[contains(text(), 'Yes, Delete')]")
        self.success_message = (By.XPATH, "//div[contains(text(), 'Successfully Deleted')]")

    def select_employee(self):
        """Selects the first employee in the list."""
        employee_card = self.wait.until(EC.presence_of_element_located(self.employee_card))
        employee_name = employee_card.text  # Capture the employee name for verification
        employee_card.click()
        return employee_name

    def delete_employee(self):
        """Deletes the selected employee."""
        self.wait.until(EC.element_to_be_clickable(self.delete_button)).click()
        self.wait.until(EC.element_to_be_clickable(self.confirm_delete_button)).click()

    def is_success_message_visible(self):
        """Checks if the success message is displayed."""
        return self.wait.until(EC.presence_of_element_located(self.success_message)).is_displayed()

    def is_employee_deleted(self, employee_name):
        """Verifies that the employee is no longer visible in the list."""
        try:
            self.wait.until(
                EC.invisibility_of_element_located((By.XPATH, f"//div[contains(text(), '{employee_name}')]"))
            )
            return True
        except TimeoutException:
            return False

import pytest
from selenium import webdriver


@pytest.fixture(scope="function")
def driver():
    """Initializes the WebDriver."""
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

import pytest
from pages.login_page import LoginPage
from pages.pim_page import PIMPage


def test_delete_employee(driver):
    """
    Test Case: Delete an employee from the PIM module.
    """
    # Test data
    url = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
    username = "Admin"
    password = "admin123"

    # Initialize Page Objects
    login_page = LoginPage(driver)
    pim_page = PIMPage(driver)

    # Step 1: Open the login page
    login_page.open(url)

    # Step 2: Log in
    login_page.login(username, password)
    assert login_page.is_pim_module_visible(), "Login failed or PIM module not visible"

    # Step 3: Navigate to the PIM module
    driver.find_element(By.XPATH, "//a[@href='/web/index.php/pim/viewPimModule']").click()

    # Step 4: Select an employee
    employee_name = pim_page.select_employee()

    # Step 5: Delete the selected employee
    pim_page.delete_employee()

    # Step 6: Verify the success message
    assert pim_page.is_success_message_visible(), "Employee deletion success message not visible"
    print("Test Passed: Employee deletion success message displayed.")

    # Step 7: Verify that the employee is deleted from the list
    assert pim_page.is_employee_deleted(employee_name), f"Employee '{employee_name}' still exists in the list."
    print("Test Passed: Employee was deleted successfully.")
