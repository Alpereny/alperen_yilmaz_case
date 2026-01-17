import pytest
from pages.home_page import HomePage


class TestHome:
    def test_home_page_opened(self, home_page: HomePage, base_url: str):
        home_page.go_to_url(base_url)

        assert home_page.get_current_url().startswith(base_url)
        assert home_page.get_title() == "Insider One | #1 Platform for AI-Powered Customer Engagement"

    @pytest.mark.parametrize("block_name", [
        "Header",
        "Navigation",
        "Logo",
        "Social Proof",
        "Core Differentiators",
        "Capabilities",
        "Insider One AI",
        "Channels",
        "Case Study",
        "Analyst",
        "Integrations",
        "Resources",
        "Call to Action",
        "Footer",
    ])
    def test_element_displayed(self, home_page: HomePage, base_url: str, block_name: str):
        home_page.go_to_url(base_url)
        locator = home_page.get_element_locator(block_name)
        home_page.scroll_to(locator)
        assert home_page.is_displayed(locator), f"'{block_name}' should be displayed"
