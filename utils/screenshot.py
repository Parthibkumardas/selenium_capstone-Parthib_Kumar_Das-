"""Screenshot helper used on test failure by both the pytest and unittest suites."""
import re
from datetime import datetime

from utils.config_reader import ConfigReader
from utils.logger import get_logger

log = get_logger("screenshot")


def take_screenshot(driver, test_name):
    """Save a PNG named after the test; returns the file path (or None on error)."""
    folder = ConfigReader.get_path("screenshots")
    folder.mkdir(parents=True, exist_ok=True)
    safe_name = re.sub(r"[^\w\-]+", "_", test_name)[-120:]
    path = folder / f"{safe_name}_{datetime.now():%Y%m%d_%H%M%S}.png"
    try:
        driver.save_screenshot(str(path))
        log.info("Screenshot saved: %s", path)
        return str(path)
    except Exception as exc:  # never let a screenshot problem hide the real failure
        log.error("Could not take screenshot: %s", exc)
        return None
