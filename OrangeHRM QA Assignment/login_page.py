"""
login_page.py

LoginPage models the OrangeHRM login screen and the post-login top-nav
user dropdown used for logout. All locators live here so a UI change only
requires an update in one place.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage

LOGIN_URL = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"


class LoginPage(BasePage):
    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")
    ERROR_ALERT = (By.XPATH, "//p[contains(@class,'oxd-alert-content-text')]")
    DASHBOARD_HEADER = (By.XPATH, "//h6[text()='Dashboard']")

    
    USER_DROPDOWN = (By.XPATH, "//span[contains(@class,'oxd-userdropdown-tab')]")
    LOGOUT_LINK = (By.XPATH, "//a[text()='Logout']")

    def load(self):
        """Navigate directly to the login page."""
        self.driver.get(LOGIN_URL)
        self.wait_visible(self.USERNAME_INPUT)
        return self

    def login(self, username: str, password: str):
        """Fill credentials and submit the login form."""
        self.type_text(self.USERNAME_INPUT, username)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        # Confirm the app navigated to the dashboard before returning control.
        self.wait_url_contains("dashboard")
        self.wait_visible(self.DASHBOARD_HEADER)
        return self

    def get_error_message(self) -> str:
        """Return the inline error text shown for invalid credentials."""
        return self.get_text(self.ERROR_ALERT)

    def logout(self):
        """Log out via the top-right user dropdown, from any authenticated page."""
        self.click(self.USER_DROPDOWN)
        self.click(self.LOGOUT_LINK)
        self.wait_visible(self.USERNAME_INPUT)  # back on the login form
        return self
