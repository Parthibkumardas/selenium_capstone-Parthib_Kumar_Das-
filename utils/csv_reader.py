"""CSV test-data handling: every row becomes a dict keyed by the header row."""
import csv
from pathlib import Path

from utils.config_reader import ConfigReader


def read_csv(file_path):
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Test data file not found: {path}")
    with open(path, newline="", encoding="utf-8-sig") as handle:
        return [
            {key.strip(): (value or "").strip() for key, value in row.items() if key}
            for row in csv.DictReader(handle)
        ]


def get_test_data(key):
    """Read the CSV registered under [paths] in config.ini (e.g. 'login_data')."""
    return read_csv(ConfigReader.get_path(key))
