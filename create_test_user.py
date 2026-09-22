"""One-time setup: registers the account used by the valid-login test case.

The credentials come from the first 'success' row of testdata/login_data.csv.
The demo site is shared by everyone, so use an e-mail address unique to you.
Usage:  python create_test_user.py [--headless]
"""
import argparse

from pages.register_page import RegisterPage
from utils.csv_reader import get_test_data
from utils.driver_factory import DriverFactory


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--headless", action="store_true")
    args = parser.parse_args()

    user = next(row for row in get_test_data("login_data") if row["expected_result"] == "success")
    driver = DriverFactory.get_driver(headless=True if args.headless else None)
    try:
        page = RegisterPage(driver).open()
        page.register("Capstone", "Tester", user["email"], "9999999999", user["password"])
        if page.is_registration_successful():
            print(f"Account created for {user['email']}")
        else:
            print(f"Registration did not succeed: {page.get_error_message()}")
            print("If the e-mail is already registered, either it is yours already or pick a new "
                  "unique e-mail in testdata/login_data.csv and run this script again.")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
