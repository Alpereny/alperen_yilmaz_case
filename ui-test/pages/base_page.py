from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import config
import time


class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, config.element_wait_timeout)

    def go_to_url(self, url: str, wait_for_load: bool = True) -> None:
        self.driver.get(url)
        if wait_for_load:
            self.wait_for_page_load()

    def get_current_url(self) -> str:
        return self.driver.current_url

    def get_title(self) -> str:
        return self.driver.title

    def get_window_handles(self) -> list[str]:
        return self.driver.window_handles

    def switch_to_tab(self, window_handle_index: int):
        self.driver.switch_to.window(self.get_window_handles()[window_handle_index])

    def close(self):
        self.driver.close()

    def find_element(
        self, locator: tuple[By, str], format_args: dict = None
    ) -> WebElement:
        if not format_args:
            return self.driver.find_element(*locator)

        by, selector = locator
        return self.driver.find_element(by, selector.format(**format_args))

    def find_elements(
        self, locator: tuple[By, str], format_args: dict = None
    ) -> list[WebElement]:
        if not format_args:
            return self.driver.find_elements(*locator)

        by, selector = locator
        return self.driver.find_elements(by, selector.format(**format_args))

    def select_by_visible_text(self, select_locator: tuple[By, str], text: str):
        from selenium.webdriver.support.ui import Select
        select_element = Select(self.find_element(select_locator))
        select_element.select_by_visible_text(text)

    def wait_for(self, lambda_expression) -> WebElement:
        return self.wait.until(lambda_expression)

    def wait_for_page_load(self) -> None:
        self.wait.until(
            lambda _: self.driver.execute_script("return document.readyState") == "complete"
        )

    def scroll_to(self, locator: tuple, wait_seconds=1, offset: int = 100) -> None:
        element = self.find_element(locator)
        self.driver.execute_script(
            """
            const element = arguments[0];
            const offset = arguments[1];
            const elementRect = element.getBoundingClientRect();
            const absoluteElementTop = elementRect.top + window.pageYOffset;
            const targetScrollPosition = absoluteElementTop - offset;
            window.scrollTo({top: targetScrollPosition, behavior: 'instant'});
            """,
            element,
            offset
        )
        time.sleep(wait_seconds)

    def hover(self, locator: tuple) -> None:
        element = self.find_element(locator)
        ActionChains(self.driver).move_to_element(element).pause(0.5).perform()

    def is_displayed(self, locator: tuple, timeout: float = None) -> bool:
        wait = WebDriverWait(self.driver, timeout) if timeout else self.wait
        element = wait.until(EC.visibility_of_element_located(locator))
        return element.is_displayed()

    def wait_for_element_to_disappear_from_dom(self, locator: tuple[By, str], timeout: int = None) -> bool:
        wait = WebDriverWait(self.driver, timeout) if timeout else self.wait
        return wait.until(EC.staleness_of(self.driver.find_element(*locator)))