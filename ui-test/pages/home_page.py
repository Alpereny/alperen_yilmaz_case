from .base_page import BasePage
from selenium.webdriver.common.by import By


class HomePage(BasePage):
    HEADER = (By.CSS_SELECTOR, "header, [role='banner']")
    NAVIGATION = (By.CSS_SELECTOR, "nav, [role='navigation']")
    LOGO = (By.CSS_SELECTOR, ".header-logo")

    SECTION_SOCIAL_PROOF = (By.CSS_SELECTOR, "section.homepage-social-proof")
    SECTION_CORE_DIFFERENTIATORS = (By.CSS_SELECTOR, "section.homepage-core-differentiators")
    SECTION_CAPABILITIES = (By.CSS_SELECTOR, "section.homepage-capabilities")
    SECTION_INSIDER_ONE_AI = (By.CSS_SELECTOR, "section.homepage-insider-one-ai")
    SECTION_CHANNELS = (By.CSS_SELECTOR, "section.homepage-channels")
    SECTION_CASE_STUDY = (By.CSS_SELECTOR, "section.homepage-case-study")
    SECTION_ANALYST = (By.CSS_SELECTOR, "section.homepage-analyst")
    SECTION_INTEGRATIONS = (By.CSS_SELECTOR, "section.homepage-integrations")
    SECTION_RESOURCES = (By.CSS_SELECTOR, "section.homepage-resources")
    SECTION_CALL_TO_ACTION = (By.CSS_SELECTOR, "section.homepage-call-to-action")

    FOOTER = (By.CSS_SELECTOR, "footer, [role='contentinfo']")

    PAGE_ELEMENTS = {
        "Header": HEADER,
        "Navigation": NAVIGATION,
        "Logo": LOGO,
        "Social Proof": SECTION_SOCIAL_PROOF,
        "Core Differentiators": SECTION_CORE_DIFFERENTIATORS,
        "Capabilities": SECTION_CAPABILITIES,
        "Insider One AI": SECTION_INSIDER_ONE_AI,
        "Channels": SECTION_CHANNELS,
        "Case Study": SECTION_CASE_STUDY,
        "Analyst": SECTION_ANALYST,
        "Integrations": SECTION_INTEGRATIONS,
        "Resources": SECTION_RESOURCES,
        "Call to Action": SECTION_CALL_TO_ACTION,
        "Footer": FOOTER,
    }


    def get_element_locator(self, element_name: str) -> tuple:
        return self.PAGE_ELEMENTS[element_name]
