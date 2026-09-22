"""PyTest fixtures and hooks: driver lifecycle, CLI options, screenshot on failure."""
import base64
from pathlib import Path

import pytest
from pytest_html import extras

from utils.config_reader import ConfigReader
from utils.driver_factory import DriverFactory
from utils.screenshot import take_screenshot


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default=None,
                     help="chrome | firefox | edge (default: value in config.ini)")
    # store_true with default=None lets us tell "flag not given" from "flag given"
    parser.addoption("--headless", action="store_true", default=None,
                     help="run the browser without a UI")


def pytest_html_report_title(report):
    report.title = "Selenium Capstone - PyTest Report"


@pytest.fixture
def driver(request):
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    web_driver = DriverFactory.get_driver(browser, headless)
    web_driver.get(ConfigReader.base_url())
    yield web_driver
    web_driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """On failure, save a screenshot and attach it to the HTML report."""
    outcome = yield
    report = outcome.get_result()
    if report.when not in ("setup", "call") or not report.failed:
        return

    web_driver = item.funcargs.get("driver")
    if web_driver is None:
        return

    path = take_screenshot(web_driver, item.name)
    if path:
        encoded = base64.b64encode(Path(path).read_bytes()).decode()
        report.extras = getattr(report, "extras", []) + [extras.png(encoded, "Failure screenshot")]
