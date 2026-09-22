import pytest

from pages.account_page import AccountPage
from pages.home_page import HomePage
from utils.csv_reader import get_test_data

LOGIN_DATA = get_test_data("login_data")
VALID_USER = next(row for row in LOGIN_DATA if row["expected_result"] == "success")


@pytest.mark.smoke
def test_login_page_loads_from_home_page(driver):
    login_page = HomePage(driver).go_to_login_page()
    assert login_page.is_loaded(), "Login form was not displayed"
    assert "Account Login" in driver.title


@pytest.mark.regression
@pytest.mark.parametrize("row", LOGIN_DATA, ids=[row["test_id"] for row in LOGIN_DATA])
def test_login_data_driven(driver, row):
    login_page = HomePage(driver).go_to_login_page()
    login_page.login(row["email"], row["password"])

    if row["expected_result"] == "success":
        assert AccountPage(driver).is_loaded(), (
            f"Valid login failed for {row['email']}. Did you run create_test_user.py?"
        )
    else:
        assert row["expected_message"] in login_page.get_error_message()


@pytest.mark.smoke
def test_logout_after_successful_login(driver):
    home_page = HomePage(driver)
    login_page = home_page.go_to_login_page()
    login_page.login(VALID_USER["email"], VALID_USER["password"])

    account_page = AccountPage(driver)
    assert account_page.is_loaded()
    account_page.logout()
    assert account_page.is_logout_successful()
