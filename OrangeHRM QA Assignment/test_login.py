"""
test_login.py

Focused automated test script for login functionality, independent of the
full PIM workflow suite. Maps to the manual test cases TC_LOGIN_01,
TC_LOGIN_02, and TC_LOGIN_04 from TEST_CASES_AND_BUGS.md.

Run with:
    pytest tests/test_login.py -v
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pages.login_page import LoginPage

VALID_USERNAME = "Admin"
VALID_PASSWORD = "admin123"


@pytest.fixture()
def driver():
    """Function-scoped driver: a fresh browser session per test for isolation."""
    drv = LoginPage.init_driver(headless=False)
    yield drv
    drv.quit()


def test_login_success_with_valid_credentials(driver):
    """TC_LOGIN_01: Valid credentials should land the user on the Dashboard."""
    login_page = LoginPage(driver).load()
    login_page.login(VALID_USERNAME, VALID_PASSWORD)
    assert "dashboard" in driver.current_url


def test_login_failure_with_invalid_password(driver):
    """TC_LOGIN_02: An incorrect password should show a generic error and
    keep the user on the login page."""
    login_page = LoginPage(driver).load()
    login_page.type_text(login_page.USERNAME_INPUT, VALID_USERNAME)
    login_page.type_text(login_page.PASSWORD_INPUT, "wrongpass1")
    login_page.click(login_page.LOGIN_BUTTON)

    error_text = login_page.get_error_message()
    assert "invalid credentials" in error_text.lower()
    assert "auth/login" in driver.current_url


def test_login_validation_on_empty_fields(driver):
    """TC_LOGIN_04: Submitting the form with empty fields should trigger
    inline required-field validation rather than a network call."""
    login_page = LoginPage(driver).load()
    login_page.click(login_page.LOGIN_BUTTON)

    from selenium.webdriver.common.by import By

    required_locator = (By.XPATH, "//span[text()='Required']")
    required_messages = login_page.wait_all_visible(required_locator)
    assert len(required_messages) >= 1, "Expected 'Required' validation messages"
    assert "auth/login" in driver.current_url
