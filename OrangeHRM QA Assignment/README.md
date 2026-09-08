# OrangeHRM QA Automation Assignment

Python + Selenium + Page Object Model (POM) automation suite for the
OrangeHRM demo application, built for the QA Engineer Assignment 2026.

## Project Structure

```
orangehrm-qa/
├── TEST_CASES_AND_BUGS.md      # Manual testing deliverable (Task 1)
├── pages/
│   ├── base_page.py            # Common Selenium utilities (waits, click, type, hover)
│   ├── login_page.py           # Login page locators + login()/logout()
│   └── pim_page.py             # PIM navigation, Add Employee, Employee List search/verify
├── tests/
│   ├── test_login.py           # Focused login test script (positive/negative)
│   └── test_orangehrm_workflow.py  # Full end-to-end workflow (login → PIM → add → verify → logout)
├── requirements.txt
├── pytest.ini
└── README.md
```

## Prerequisites

- Python 3.9+
- Google Chrome installed (Selenium Manager auto-resolves the matching
  chromedriver as of Selenium 4.6+, so no manual driver download is needed)

## Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running the Tests

Run the full end-to-end workflow (login, add 3 employees, verify each in
the Employee List, logout) — use `-s` to see the "Name Verified" output:

```bash
pytest tests/test_orangehrm_workflow.py -v -s
```

Run the focused login test script only:

```bash
pytest tests/test_login.py -v
```

Run everything:

```bash
pytest -v -s
```

## Design Notes

- **Page Object Model**: `BasePage` holds all reusable Selenium
  primitives (explicit waits, click, type, hover, scroll). `LoginPage`
  and `PimPage` extend it and expose only business-readable methods
  (`login()`, `add_employee()`, `is_employee_listed()`), keeping locators
  and low-level Selenium calls out of the test scripts.
- **No hardcoded sleeps**: every wait is an explicit `WebDriverWait`
  condition (`visibility_of_element_located`, `element_to_be_clickable`,
  `url_contains`, `invisibility_of_element_located`), which is faster and
  more reliable than `time.sleep()`.
- **Sequential, stateful tests**: `test_orangehrm_workflow.py` uses a
  module-scoped fixture so the same browser session and the list of added
  employee names carry across steps, mirroring a real user journey rather
  than isolated unit tests.
- **Credentials**: hardcoded as constants (`Admin` / `admin123`) since
  they are the publicly documented demo credentials on the login page
  itself. In a production suite these would be pulled from environment
  variables or a secrets manager instead.
