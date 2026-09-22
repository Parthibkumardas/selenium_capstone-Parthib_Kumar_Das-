"""Runs the unittest suite and writes an HTML report to reports/.

Usage:  python run_unittest.py [--browser firefox] [--headless] [--pattern "test_login*.py"]
"""
import argparse
import os
import sys
import unittest
from datetime import datetime

from utils.config_reader import ROOT_DIR, ConfigReader
from utils.html_reporter import HtmlTestResult, write_html_report


def main():
    parser = argparse.ArgumentParser(description="Run unittest suite with HTML report")
    parser.add_argument("--browser", help="chrome | firefox | edge")
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--pattern", default="test_*.py")
    args = parser.parse_args()

    # ConfigReader gives environment variables priority over config.ini
    if args.browser:
        os.environ["BROWSER"] = args.browser
    if args.headless:
        os.environ["HEADLESS"] = "true"

    start_dir = ROOT_DIR / "tests" / "unittest_tests"
    suite = unittest.defaultTestLoader.discover(
        str(start_dir), pattern=args.pattern, top_level_dir=str(ROOT_DIR)
    )
    result = unittest.TextTestRunner(verbosity=2, resultclass=HtmlTestResult).run(suite)

    report = ConfigReader.get_path("reports") / f"unittest_report_{datetime.now():%Y%m%d_%H%M%S}.html"
    write_html_report(result.records, report, "Selenium Capstone - Unittest Report")
    print(f"\nHTML report: {report}")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
