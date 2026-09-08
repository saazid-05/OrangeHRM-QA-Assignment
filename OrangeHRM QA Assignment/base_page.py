"""
base_page.py

BasePage encapsulates common Selenium WebDriver utilities shared across all
Page Objects: browser setup, explicit waits, and reusable interaction
primitives (click, input, hover). All concrete page classes inherit from
this class rather than duplicating boilerplate.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

DEFAULT_TIMEOUT = 15  # seconds, used for all explicit waits


class BasePage:
    """Common functionality shared by every Page Object in the suite."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, DEFAULT_TIMEOUT)

    @staticmethod
    def init_driver(headless: bool = False):
        """
        Create and return a configured Chrome WebDriver instance.
        Selenium 4.6+ ships with Selenium Manager, which resolves the
        correct chromedriver automatically -- no manual driver path needed.
        """
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")

        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(0)  # rely exclusively on explicit waits
        return driver

    def wait_visible(self, locator):
        """Wait until the element located by `locator` is visible; return it."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_clickable(self, locator):
        """Wait until the element located by `locator` is clickable; return it."""
        return self.wait.until(EC.element_to_be_clickable(locator))

    def wait_all_visible(self, locator):
        """Wait until all elements matching `locator` are visible; return list."""
        return self.wait.until(EC.visibility_of_all_elements_located(locator))

    def wait_url_contains(self, fragment):
        """Wait until the current URL contains the given fragment."""
        return self.wait.until(EC.url_contains(fragment))

    def wait_invisible(self, locator):
        """Wait until the element located by `locator` becomes invisible/absent.
        Useful for waiting out the OrangeHRM loading spinner overlay."""
        return self.wait.until(EC.invisibility_of_element_located(locator))

    def click(self, locator):
        """Wait for an element to be clickable, then click it."""
        element = self.wait_clickable(locator)
        element.click()
        return element

    def type_text(self, locator, text: str, clear_first: bool = True):
        """Wait for an input to be visible, optionally clear it, then type."""
        element = self.wait_visible(locator)
        if clear_first:
            element.clear()
        element.send_keys(text)
        return element

    def get_text(self, locator) -> str:
        """Return the visible text of an element, waiting for it first."""
        return self.wait_visible(locator).text

    def hover(self, locator):
        """Move the mouse over an element (used for dropdown/menu reveals)."""
        element = self.wait_visible(locator)
        ActionChains(self.driver).move_to_element(element).perform()
        return element

    def is_element_present(self, locator, timeout: int = 5) -> bool:
        """Return True if the element appears within `timeout` seconds."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def scroll_into_view(self, element):
        """Scroll the page so the given WebElement is in the visible viewport."""
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )
