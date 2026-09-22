from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):
    PATH = "index.php?route=account/login"

    RETURNING_CUSTOMER_HEADING = (By.XPATH, "//h2[normalize-space()='Returning Customer']")
    EMAIL_INPUT = (By.ID, "input-email")
    PASSWORD_INPUT = (By.ID, "input-password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "input[value='Login']")
    ERROR_ALERT = (By.CSS_SELECTOR, "div.alert-danger")

    def open(self):
        self.open_path(self.PATH)
        return self

    def is_loaded(self):
        return self.is_displayed(self.RETURNING_CUSTOMER_HEADING) and self.is_displayed(self.LOGIN_BUTTON)

    def login(self, email, password):
        self.type_text(self.EMAIL_INPUT, email)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def get_error_message(self):
        return self.get_text(self.ERROR_ALERT)
