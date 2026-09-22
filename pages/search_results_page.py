from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class SearchResultsPage(BasePage):
    HEADING = (By.XPATH, "//div[@id='content']/h1[starts-with(normalize-space(),'Search')]")
    PRODUCT_NAMES = (By.CSS_SELECTOR, "#content .product-layout .caption h4 a")
    NO_RESULT_MESSAGE = (
        By.XPATH, "//div[@id='content']//p[contains(normalize-space(),'no product that matches')]"
    )

    def wait_for_results(self):
        """The page shows either product tiles or a 'no product' message; wait for one."""
        self.wait.until(
            EC.any_of(
                EC.presence_of_element_located(self.PRODUCT_NAMES),
                EC.presence_of_element_located(self.NO_RESULT_MESSAGE),
            )
        )

    def get_heading(self):
        return self.get_text(self.HEADING)

    def get_product_names(self):
        self.wait_for_results()
        return [element.text.strip() for element in self.driver.find_elements(*self.PRODUCT_NAMES)]

    def has_no_results(self):
        self.wait_for_results()
        return bool(self.driver.find_elements(*self.NO_RESULT_MESSAGE))

    def get_no_result_message(self):
        return self.get_text(self.NO_RESULT_MESSAGE)
