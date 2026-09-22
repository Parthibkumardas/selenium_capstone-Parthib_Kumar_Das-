from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.login_page import LoginPage
from pages.search_results_page import SearchResultsPage


class HomePage(BasePage):
    SEARCH_INPUT = (By.CSS_SELECTOR, "#search input[name='search']")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "#search button")
    MY_ACCOUNT_MENU = (By.XPATH, "//a[@title='My Account']")
    LOGIN_LINK = (By.XPATH, "//ul[contains(@class,'dropdown-menu')]//a[normalize-space()='Login']")

    def open(self):
        self.open_path("")
        return self

    def search_for(self, term):
        self.type_text(self.SEARCH_INPUT, term)
        self.click(self.SEARCH_BUTTON)
        return SearchResultsPage(self.driver)

    def go_to_login_page(self):
        self.click(self.MY_ACCOUNT_MENU)
        self.click(self.LOGIN_LINK)
        return LoginPage(self.driver)
