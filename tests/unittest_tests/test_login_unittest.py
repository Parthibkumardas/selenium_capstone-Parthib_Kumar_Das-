from pages.account_page import AccountPage
from pages.home_page import HomePage
from tests.unittest_tests.base_test import BaseTest
from utils.csv_reader import get_test_data

LOGIN_DATA = get_test_data("login_data")
VALID_USER = next(row for row in LOGIN_DATA if row["expected_result"] == "success")


class LoginUnittest(BaseTest):

    def test_login_page_loads_from_home_page(self):
        login_page = HomePage(self.driver).go_to_login_page()
        self.assertTrue(login_page.is_loaded(), "Login form was not displayed")
        self.assertIn("Account Login", self.driver.title)

    def test_logout_after_successful_login(self):
        login_page = HomePage(self.driver).go_to_login_page()
        login_page.login(VALID_USER["email"], VALID_USER["password"])
        account_page = AccountPage(self.driver)
        self.assertTrue(account_page.is_loaded())
        account_page.logout()
        self.assertTrue(account_page.is_logout_successful())


def _build_login_test(row):
    def test(self):
        login_page = HomePage(self.driver).go_to_login_page()
        login_page.login(row["email"], row["password"])
        if row["expected_result"] == "success":
            self.assertTrue(AccountPage(self.driver).is_loaded(),
                            f"Valid login failed for {row['email']}. Run create_test_user.py first.")
        else:
            self.assertIn(row["expected_message"], login_page.get_error_message())
    return test


# One real test method per CSV row, so each row gets its own browser, result and screenshot.
for _row in LOGIN_DATA:
    setattr(LoginUnittest, f"test_{_row['test_id'].lower()}_data_driven", _build_login_test(_row))
