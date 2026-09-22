"""Creates WebDriver instances. Selenium 4.6+ downloads matching drivers itself."""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from utils.config_reader import ConfigReader
from utils.logger import get_logger

log = get_logger("driver_factory")


class DriverFactory:
    @staticmethod
    def get_driver(browser=None, headless=None):
        browser = (browser or ConfigReader.browser()).lower()
        headless = ConfigReader.headless() if headless is None else headless
        log.info("Starting %s (headless=%s)", browser, headless)

        if browser == "chrome":
            options = ChromeOptions()
            options.add_argument("--disable-notifications")
            options.add_argument("--window-size=1920,1080")
            if headless:
                options.add_argument("--headless=new")
                options.add_argument("--no-sandbox")
            driver = webdriver.Chrome(options=options)
        elif browser == "firefox":
            options = FirefoxOptions()
            if headless:
                options.add_argument("-headless")
            driver = webdriver.Firefox(options=options)
        elif browser == "edge":
            options = EdgeOptions()
            options.add_argument("--window-size=1920,1080")
            if headless:
                options.add_argument("--headless=new")
            driver = webdriver.Edge(options=options)
        else:
            raise ValueError(f"Unsupported browser '{browser}'. Use chrome, firefox or edge.")

        if not headless:
            driver.maximize_window()
        driver.set_page_load_timeout(ConfigReader.page_load_timeout())
        return driver
