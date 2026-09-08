"""
test_orangehrm_workflow.py

End-to-end pytest suite for the OrangeHRM automation assignment.

Workflow under test:
    1. Launch browser, navigate to the login page.
    2. Log in with valid credentials (Admin / admin123).
    3. Hover over and click the PIM module.
    4. Add 3 distinct employees.
    5. Navigate to the Employee List, search/paginate to locate each
       employee, verify their name, and print "Name Verified" for each.
    6. Log out and close the browser.

Run with:
    pytest tests/test_orangehrm_workflow.py -v -s
    (the -s flag is required to see the "Name Verified" console output)
"""

import sys
import os
import pytest

# Allow `pages` package to be imported when running pytest from the repo root.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pages.login_page import LoginPage
from pages.pim_page import PimPage

VALID_USERNAME = "Admin"
VALID_PASSWORD = "admin123"

# Realistic dummy employees to add during the run.
EMPLOYEES_TO_ADD = [
    ("John", "Doe"),
    ("Jane", "Smith"),
    ("Alex", "Jones"),
]


@pytest.fixture(scope="module")
def driver():
    """Module-scoped WebDriver: one browser session for the whole workflow."""
    drv = LoginPage.init_driver(headless=False)
    yield drv
    drv.quit()


@pytest.fixture(scope="module")
def added_employee_names():
    """Shared list of full names successfully added, used by later tests."""
    return []


class TestOrangeHRMWorkflow:
    """
    Tests are ordered and share browser state (module-scoped `driver`) so
    that employees added in one step can be verified in a later step,
    mirroring a real sequential user journey rather than isolated units.
    """

    def test_01_login_with_valid_credentials(self, driver):
        """Log in and confirm the Dashboard loads."""
        login_page = LoginPage(driver).load()
        login_page.login(VALID_USERNAME, VALID_PASSWORD)
        assert "dashboard" in driver.current_url, "Did not land on the Dashboard after login"

    def test_02_navigate_to_pim_module(self, driver):
        """Hover over and click the PIM nav item."""
        pim_page = PimPage(driver)
        pim_page.open_pim_module()
        assert "pim" in driver.current_url, "PIM module did not load"

    def test_03_add_three_employees(self, driver, added_employee_names):
        """Add three distinct employees via the Add Employee form."""
        pim_page = PimPage(driver)
        for first_name, last_name in EMPLOYEES_TO_ADD:
            pim_page.go_to_add_employee()
            pim_page.add_employee(first_name, last_name)
            full_name = f"{first_name} {last_name}"
            added_employee_names.append(full_name)
            print(f"Added employee: {full_name}")

            # Return to the PIM landing page before adding the next employee.
            pim_page.open_pim_module()

        assert len(added_employee_names) == 3, "Not all 3 employees were added"

    def test_04_verify_employees_in_employee_list(self, driver, added_employee_names):
        """
        Navigate to the Employee List, search for each added employee,
        paginate/scroll as needed, and print 'Name Verified' for each match.
        """
        pim_page = PimPage(driver)
        pim_page.open_pim_module()
        pim_page.go_to_employee_list()

        assert added_employee_names, "No employees were added in the previous step"

        for full_name in added_employee_names:
            pim_page.search_employee_by_name(full_name)
            found = pim_page.is_employee_listed(full_name)
            assert found, f"Employee '{full_name}' was not found in the Employee List"
            print("Name Verified")

    def test_05_logout(self, driver):
        """Log out of the application and confirm the login form reappears."""
        login_page = LoginPage(driver)
        login_page.logout()
        assert "auth/login" in driver.current_url, "Logout did not return to the login page"
