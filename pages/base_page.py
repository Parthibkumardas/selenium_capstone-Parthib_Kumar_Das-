"""Parent of every page object: wraps Selenium with explicit waits and logging."""
from urllib.parse import urljoin

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.config_reader import ConfigReader
from utils.logger import get_logger


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, ConfigReader.explicit_wait())
        self.log = get_logger(self.__class__.__name__)

    def open_path(self, path=""):
        url = urljoin(ConfigReader.base_url(), path)
        self.log.info("Opening %s", url)
        self.driver.get(url)

    def find(self, locator):
        return self.wait.until(
            EC.visibility_of_element_located(locator),
            message=f"Element not visible: {locator}",
        )

    def click(self, locator):
        self.log.info("Click %s", locator)
        self.wait.until(
            EC.element_to_be_clickable(locator),
            message=f"Element not clickable: {locator}",
        ).click()

    def type_text(self, locator, text, clear=True):
        # The text is deliberately not logged so passwords never reach the log file.
        self.log.info("Type into %s", locator)
        element = self.find(locator)
        if clear:
            element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        return self.find(locator).text.strip()

    def is_displayed(self, locator, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    @property
    def title(self):
        return self.driver.title

    @property
    def current_url(self):
        return self.driver.current_url
