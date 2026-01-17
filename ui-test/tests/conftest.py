import pytest
from pages.home_page import HomePage


@pytest.fixture(scope="function")
def home_page(driver):
    return HomePage(driver)
