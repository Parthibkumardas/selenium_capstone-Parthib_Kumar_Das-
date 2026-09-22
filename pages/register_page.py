from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class RegisterPage(BasePage):
    """Used only by create_test_user.py to prepare the account for the valid-login test."""
    PATH = "index.php?route=account/register"

    FIRST_NAME = (By.ID, "input-firstname")
    LAST_NAME = (By.ID, "input-lastname")
    EMAIL = (By.ID, "input-email")
    TELEPHONE = (By.ID, "input-telephone")
    PASSWORD = (By.ID, "input-password")
    CONFIRM = (By.ID, "input-confirm")
    AGREE = (By.NAME, "agree")
    CONTINUE = (By.CSS_SELECTOR, "input[value='Continue']")
    SUCCESS_HEADING = (By.XPATH, "//div[@id='content']/h1[contains(.,'Your Account Has Been Created')]")
    ERROR_ALERT = (By.CSS_SELECTOR, "div.alert-danger")

    def open(self):
        self.open_path(self.PATH)
        return self

    def register(self, first_name, last_name, email, telephone, password):
        self.type_text(self.FIRST_NAME, first_name)
        self.type_text(self.LAST_NAME, last_name)
        self.type_text(self.EMAIL, email)
        self.type_text(self.TELEPHONE, telephone)
        self.type_text(self.PASSWORD, password)
        self.type_text(self.CONFIRM, password)
        self.click(self.AGREE)
        self.click(self.CONTINUE)

    def is_registration_successful(self):
        return self.is_displayed(self.SUCCESS_HEADING)

    def get_error_message(self):
        return self.get_text(self.ERROR_ALERT)
