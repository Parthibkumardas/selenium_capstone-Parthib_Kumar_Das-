"""Base class for unittest tests: browser lifecycle + screenshot on failure."""
import unittest

from utils.config_reader import ConfigReader
from utils.driver_factory import DriverFactory
from utils.screenshot import take_screenshot


class BaseTest(unittest.TestCase):
    screenshot_path = None

    def setUp(self):
        self.driver = DriverFactory.get_driver()
        self.driver.get(ConfigReader.base_url())

    def tearDown(self):
        try:
            if self._test_failed():
                self.screenshot_path = take_screenshot(self.driver, self.id())
        finally:
            self.driver.quit()

    def _test_failed(self):
        """True if the current test has failed/errored so far (works on Python 3.9 - 3.13)."""
        outcome = getattr(self, "_outcome", None)
        if outcome is None:
            return False
        if hasattr(outcome, "errors"):  # Python <= 3.10
            result = self.defaultTestResult()
            self._feedErrorsToResult(result, outcome.errors)
        else:  # Python >= 3.11
            result = outcome.result
        problems = list(getattr(result, "failures", [])) + list(getattr(result, "errors", []))
        return any(getattr(test, "test_case", test) is self for test, _ in problems)
