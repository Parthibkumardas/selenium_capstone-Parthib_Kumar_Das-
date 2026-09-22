"""Central place for reading config/config.ini.

Environment variables (BASE_URL, BROWSER, HEADLESS) override the ini file,
which makes the framework CI-friendly without editing any file.
"""
import configparser
import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE = ROOT_DIR / "config" / "config.ini"


class ConfigReader:
    _parser = None

    @classmethod
    def _config(cls):
        if cls._parser is None:
            parser = configparser.ConfigParser()
            if not parser.read(CONFIG_FILE, encoding="utf-8"):
                raise FileNotFoundError(f"Config file not found: {CONFIG_FILE}")
            cls._parser = parser
        return cls._parser

    @classmethod
    def get(cls, section, key, env_var=None):
        if env_var and os.getenv(env_var):
            return os.environ[env_var]
        return cls._config().get(section, key)

    @classmethod
    def base_url(cls):
        url = cls.get("application", "base_url", "BASE_URL").strip()
        return url if url.endswith("/") else url + "/"

    @classmethod
    def browser(cls):
        return cls.get("browser", "name", "BROWSER").strip().lower()

    @classmethod
    def headless(cls):
        return cls.get("browser", "headless", "HEADLESS").strip().lower() in {"1", "true", "yes"}

    @classmethod
    def explicit_wait(cls):
        return int(cls.get("browser", "explicit_wait"))

    @classmethod
    def page_load_timeout(cls):
        return int(cls.get("browser", "page_load_timeout"))

    @classmethod
    def get_path(cls, key):
        """Resolve a value from the [paths] section relative to the project root."""
        return ROOT_DIR / cls.get("paths", key)
