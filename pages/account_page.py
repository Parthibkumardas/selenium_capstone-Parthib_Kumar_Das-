from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class AccountPage(BasePage):
    HEADING = (By.XPATH, "//div[@id='content']//h2[normalize-space()='My Account']")
    # The right sidebar is an <aside id="column-right">, so the locator must not assume a <div>
    LOGOUT_LINK = (By.XPATH, "//*[@id='column-right']//a[normalize-space()='Logout']")
    LOGOUT_HEADING = (By.XPATH, "//div[@id='content']//h1[normalize-space()='Account Logout']")

    def is_loaded(self):
        return self.is_displayed(self.HEADING)

    def logout(self):
        self.click(self.LOGOUT_LINK)

    def is_logout_successful(self):
        return self.is_displayed(self.LOGOUT_HEADING)