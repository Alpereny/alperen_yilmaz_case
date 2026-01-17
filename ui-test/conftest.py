import pytest
import allure
from datetime import datetime
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from config import config


@pytest.fixture(scope="session")
def driver_type():
    return config.driver_type


@pytest.fixture(scope="session")
def base_url():
    return config.base_url


def _create_local_driver(driver_type: str) -> WebDriver:
    """Create a local WebDriver instance."""
    if driver_type.lower() == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--window-size=1920,1080")
        if config.headless:
            options.add_argument("--headless")
        return webdriver.Chrome(options=options)

    elif driver_type.lower() == "firefox":
        options = webdriver.FirefoxOptions()
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        if config.headless:
            options.add_argument("--headless")
        return webdriver.Firefox(options=options)

    else:
        raise ValueError(f"Unsupported driver type: {driver_type}")


def _create_remote_driver(driver_type: str) -> WebDriver:
    """Create a remote WebDriver instance for Selenium Grid."""
    if driver_type.lower() == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--window-size=1920,1080")
        if config.headless:
            options.add_argument("--headless")
    elif driver_type.lower() == "firefox":
        options = webdriver.FirefoxOptions()
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        if config.headless:
            options.add_argument("--headless")
    else:
        raise ValueError(f"Unsupported driver type: {driver_type}")

    return webdriver.Remote(
        command_executor=config.selenium_grid_url,
        options=options
    )


@pytest.fixture(scope="function")
def driver(driver_type, base_url, request):
    driver = None

    if config.use_remote_driver:
        driver = _create_remote_driver(driver_type)
    else:
        driver = _create_local_driver(driver_type)

    driver.maximize_window()
    driver.implicitly_wait(config.implicit_wait_timeout)

    driver.get(base_url)
    driver.add_cookie({"name": "viewed_cookie_policy", "value": "no"})
    driver.refresh()

    # Store session_id for video link
    session_id = driver.session_id
    
    yield driver

    # Attach embedded video player to Allure after test completes
    if config.use_remote_driver:
        video_url = f"{config.minio_endpoint}/videos/{session_id}.mp4"
        video_html = f"""
        <html>
        <body>
            <video width="100%" height="600px" controls autoplay>
                <source src="{video_url}" type="video/mp4">
                Your browser does not support the video tag.
            </video>
        </body>
        </html>
        """
        allure.attach(
            video_html,
            name="Test Video Recording",
            attachment_type=allure.attachment_type.HTML
        )

    driver.quit()


def _capture_screenshot(driver, item) -> Path | None:
    """Capture screenshot on test failure."""
    screenshots_dir = Path(config.screenshot_dir)
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    test_name = item.name.replace(" ", "_").replace("[", "_").replace("]", "_")
    screenshot_name = f"{test_name}_{timestamp}.png"
    screenshot_path = screenshots_dir / screenshot_name

    try:
        driver.save_screenshot(str(screenshot_path))
        return screenshot_path
    except (OSError, IOError) as e:
        print(f"\nFailed to capture screenshot: {e}")
        return None


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver and config.screenshot_on_failure:
            screenshot_path = _capture_screenshot(driver, item)
            if screenshot_path:
                print(f"\nScreenshot saved: {screenshot_path}")
                # Attach screenshot to Allure report
                with open(screenshot_path, "rb") as f:
                    allure.attach(
                        f.read(),
                        name="Screenshot on Failure",
                        attachment_type=allure.attachment_type.PNG
                    )
