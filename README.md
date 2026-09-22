
Video Demonstration Link : https://www.loom.com/share/8d5cbc9d342648b9b790a8c2944b7147 

# Selenium Python Framework - Unittest + PyTest + POM

Automates **Login** and **Product Search** on the TutorialsNinja demo store
(https://tutorialsninja.com/demo/).

## Project structure

```
selenium_capstone/
├── config/config.ini            # URL, browser, waits, folder paths
├── pages/                       # Page Object Model
│   ├── base_page.py             #   waits, click, type, logging (parent class)
│   ├── home_page.py             #   header search + navigation to login
│   ├── login_page.py
│   ├── account_page.py          #   "My Account" + logout
│   ├── search_results_page.py
│   └── register_page.py         #   only used by create_test_user.py
├── utils/                       # Utility classes
│   ├── config_reader.py         #   reads config.ini (env vars override)
│   ├── driver_factory.py        #   chrome / firefox / edge, headless option
│   ├── csv_reader.py            #   CSV -> list of dicts
│   ├── screenshot.py            #   screenshot helper
│   ├── logger.py                #   console + logs/automation.log
│   └── html_reporter.py         #   HTML report for unittest
├── testdata/                    # login_data.csv, search_data.csv
├── tests/
│   ├── pytest_tests/            #   conftest.py (fixture + failure hook) + tests
│   └── unittest_tests/          #   base_test.py + tests
├── reports/                     # HTML reports + screenshots/
├── logs/
├── run_unittest.py              # unittest runner + HTML report
├── create_test_user.py          # one-time account setup
├── pytest.ini
└── requirements.txt
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt    # Python 3.9+, Chrome/Firefox/Edge installed
```
Selenium 4.6+ downloads the browser driver automatically (no webdriver-manager needed).

**One-time test-user setup.** The demo site is shared by everyone, so first open
`testdata/login_data.csv` and change the email in row `TC_LOGIN_01` to an address unique to
you, then run:

```bash
python create_test_user.py
```

## Running the tests

```bash
# PyTest (HTML report: reports/pytest_report.html)
pytest
pytest -m smoke
pytest --browser firefox --headless
pytest tests/pytest_tests/test_login_pytest.py -k TC_LOGIN_02

# Unittest (HTML report: reports/unittest_report_<timestamp>.html)
python run_unittest.py
python run_unittest.py --browser edge --headless --pattern "test_login*.py"
```

## How each requirement is covered

| Requirement | Where |
|---|---|
| Unittest | `tests/unittest_tests/`, `run_unittest.py` |
| PyTest | `tests/pytest_tests/`, `pytest.ini` |
| Page Object Model | `pages/` - locators and actions live only here, never in tests |
| Utility classes | `utils/` |
| Configuration management | `config/config.ini` + `ConfigReader`; env vars `BASE_URL`, `BROWSER`, `HEADLESS`; pytest flags `--browser`, `--headless` |
| CSV test data | `testdata/*.csv` read by `csv_reader.py`; `parametrize` in pytest, one generated test method per row in unittest |
| Screenshot on failure | pytest: `pytest_runtest_makereport` hook in `conftest.py`; unittest: `BaseTest.tearDown` |
| HTML reporting | pytest: `pytest-html` (self-contained, screenshot embedded); unittest: `html_reporter.py` |
| Logging | `utils/logger.py` -> `logs/automation.log` (passwords are never logged) |

## Design notes (useful for the viva)

- **Explicit waits only** - no `time.sleep`, no implicit wait (mixing the two causes unpredictable timeouts).
- **Fresh browser per test** - tests are independent and can run in any order.
- **POM navigation methods return the next page object**, e.g. `HomePage.search_for()` returns `SearchResultsPage`.
- **Data-driven unittest** - `unittest` has no `parametrize`, so a factory function adds one test method per
  CSV row. Each row gets its own result line, browser and screenshot (unlike `subTest`).
- **Failure detection in unittest** - `BaseTest._test_failed()` inspects the test outcome inside `tearDown`,
  before the browser closes, so the screenshot shows the real failing page.

## Notes and limitations

- The demo is a public shared site; if it is slow or resets its database, rerun `create_test_user.py`.
- OpenCart temporarily locks an account after several failed logins with the same e-mail. The negative
  login rows therefore use non-existent e-mails rather than a wrong password for the real account.
- Locators were written from the standard OpenCart 3 markup that TutorialsNinja uses. If the site changes
  its markup, only the locator constants in `pages/` need updating.
