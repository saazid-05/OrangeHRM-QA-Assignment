"""
pim_page.py

PimPage models the PIM module: the top-nav hover/click entry point, the
"Add Employee" form, and the "Employee List" search/results grid used to
verify that newly added employees are present.
"""

import time
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class PimPage(BasePage):
   
    PIM_MENU_ITEM = (By.XPATH, "//span[text()='PIM']/parent::a")
    LOADING_SPINNER = (By.CLASS_NAME, "oxd-loading-spinner")

    
    ADD_EMPLOYEE_BUTTON = (By.XPATH, "//button[contains(.,'Add')]")
    EMPLOYEE_LIST_TAB = (By.XPATH, "//a[contains(.,'Employee List')]")
    EMPLOYEE_NAME_SEARCH_INPUT = (
        By.XPATH,
        "//label[text()='Employee Name']/../..//input",
    )
    SEARCH_BUTTON = (By.XPATH, "//button[@type='submit']")
    RESET_BUTTON = (By.XPATH, "//button[contains(.,'Reset')]")
    RESULT_TABLE_ROWS = (By.XPATH, "//div[@class='oxd-table-body']/div")
    RESULT_EMPLOYEE_NAME_CELLS = (
        By.XPATH,
        "//div[@class='oxd-table-body']//div[contains(@class,'oxd-table-cell')][3]",
    )
    NO_RECORDS_FOUND = (By.XPATH, "//span[text()='No Records Found']")
    NEXT_PAGE_BUTTON = (By.XPATH, "//button[contains(@class,'oxd-pagination-page-next') and not(@disabled)]")

    FIRST_NAME_INPUT = (By.NAME, "firstName")
    LAST_NAME_INPUT = (By.NAME, "lastName")
    SAVE_BUTTON = (By.XPATH, "//button[@type='submit']")
    EMPLOYEE_FULL_NAME_HEADER = (By.XPATH, "//h6[contains(@class,'oxd-text--h6')]")

    
    def open_pim_module(self):
        """Hover over the PIM nav item, then click it, per the required workflow."""
        self.hover(self.PIM_MENU_ITEM)
        self.click(self.PIM_MENU_ITEM)
        self.wait_url_contains("pim")
        return self

    def go_to_add_employee(self):
        """From the PIM landing page, open the Add Employee form."""
        self.click(self.ADD_EMPLOYEE_BUTTON)
        self.wait_visible(self.FIRST_NAME_INPUT)
        return self

    def go_to_employee_list(self):
        """From anywhere in PIM, navigate to the Employee List tab."""
        self.click(self.EMPLOYEE_LIST_TAB)
        self.wait_visible(self.EMPLOYEE_NAME_SEARCH_INPUT)
        self._wait_for_spinner_to_clear()
        return self

    
    def add_employee(self, first_name: str, last_name: str):
        """
        Fill and submit the Add Employee form with a first/last name.
        Waits for navigation to the new employee's Personal Details page,
        which confirms the save succeeded.
        """
        self.type_text(self.FIRST_NAME_INPUT, first_name)
        self.type_text(self.LAST_NAME_INPUT, last_name)
        self.click(self.SAVE_BUTTON)
        # A successful save redirects to /pim/viewEmployees/empNumber/...
        self.wait_url_contains("viewPersonalDetails")
        self._wait_for_spinner_to_clear()
        return self


    def search_employee_by_name(self, full_name: str):
        """Search the Employee List grid by the employee's full name."""
        self.type_text(self.EMPLOYEE_NAME_SEARCH_INPUT, full_name)
        self.click(self.SEARCH_BUTTON)
        self._wait_for_spinner_to_clear()
        return self

    def is_employee_listed(self, full_name: str, max_pages: int = 5) -> bool:
        """
        Check whether `full_name` appears in the current (already-searched)
        Employee List results, paginating forward if necessary.
        Returns True as soon as a match is found; False if exhausted.
        """
        for _ in range(max_pages):
            if self.is_element_present(self.NO_RECORDS_FOUND, timeout=3):
                return False

            rows = self.wait_all_visible(self.RESULT_EMPLOYEE_NAME_CELLS)
            for row in rows:
                self.scroll_into_view(row)
                if full_name.strip().lower() in row.text.strip().lower():
                    return True

            # Try the next page if pagination controls allow it.
            if self.is_element_present(self.NEXT_PAGE_BUTTON, timeout=3):
                self.click(self.NEXT_PAGE_BUTTON)
                self._wait_for_spinner_to_clear()
            else:
                break
        return False

   
    def _wait_for_spinner_to_clear(self):
        """
        OrangeHRM shows a brief loading spinner during grid/network operations.
        Wait for it to disappear (if present) instead of using time.sleep().
        """
        try:
            self.wait_invisible(self.LOADING_SPINNER)
        except Exception:
            # Spinner may never have appeared for very fast responses; that's fine.
            pass
