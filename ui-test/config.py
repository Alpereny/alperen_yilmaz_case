import os
from pathlib import Path
import tomllib


class Config:
    def __init__(self, config_file: str = "pyproject.toml"):
        self.config_file = config_file
        self._config_data = self._load_config()

    def _load_config(self):
        config_dir = Path(__file__).parent
        config_path = config_dir / self.config_file

        with open(config_path, "rb") as f:
            data = tomllib.load(f)

        return data.get("tool", {}).get("ui-test-config", {})

    def get(self, key: str, default=None):
        env_key = f"UI_TEST_{key.upper()}"
        env_value = os.getenv(env_key)

        if env_value is not None:
            return env_value

        return self._config_data.get(key, default)

    @property
    def driver_type(self):
        return self.get("driver_type", "chrome")

    @property
    def base_url(self):
        return self.get("base_url", "https://insiderone.com")

    @property
    def qa_careers_url(self):
        return self.get("qa_careers_url", "https://insiderone.com/careers/quality-assurance/")

    @property
    def headless(self):
        value = self.get("headless", False)
        if isinstance(value, str):
            return value.lower() in ("true", "1", "yes")
        return value

    @property
    def implicit_wait_timeout(self):
        return int(self.get("implicit_wait_timeout", 30))

    @property
    def element_wait_timeout(self):
        return int(self.get("element_wait_timeout", 15))

    @property
    def screenshot_dir(self):
        return self.get("screenshot_dir", "reports/screenshots")

    @property
    def screenshot_on_failure(self):
        value = self.get("screenshot_on_failure", True)
        if isinstance(value, str):
            return value.lower() in ("true", "1", "yes")
        return value

    @property
    def selenium_grid_url(self):
        """Selenium Grid URL for remote execution. If set, tests run on grid instead of local."""
        return os.getenv("SELENIUM_GRID_URL", self.get("selenium_grid_url", None))

    @property
    def use_remote_driver(self):
        """Check if remote driver should be used."""
        return self.selenium_grid_url is not None

    @property
    def minio_endpoint(self):
        """MinIO endpoint for video links."""
        return os.getenv("MINIO_ENDPOINT", "http://localhost:9000")


config = Config()
