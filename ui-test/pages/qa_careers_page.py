from .base_page import BasePage
from selenium.webdriver.common.by import By
from config import config


class QACareersPage(BasePage):
    SEE_ALL_QA_JOBS_LINK = (By.XPATH, "//a[contains(text(), 'See all QA jobs')]")
    
    LOCATION_FILTER = (By.CSS_SELECTOR, "#filter-by-location")
    DEPARTMENT_FILTER = (By.CSS_SELECTOR, "#filter-by-department")
    
    NO_POSITIONS_MESSAGE = (By.XPATH, "//*[contains(text(), 'No positions available')]")
    
    JOB_LIST = (By.CSS_SELECTOR, ".position-list-item")
    VIEW_ROLE_BUTTON = (By.CSS_SELECTOR, "a[href*='lever.co']")
    
    JOB_POSITION_TITLE = (By.CSS_SELECTOR, ".position-title")
    JOB_POSITION_DEPARTMENT = (By.CSS_SELECTOR, ".position-department")
    JOB_POSITION_LOCATION = (By.CSS_SELECTOR, ".position-location")
    
    def go_to_qa_careers(self) -> None:
        self.go_to_url(config.qa_careers_url)
    
    def click_see_all_qa_jobs_button(self) -> None:
        self.find_element(self.SEE_ALL_QA_JOBS_LINK).click()
    
    def wait_for_jobs_to_load(self, timeout: int = 50) -> None:
        try:
            self.wait_for_element_to_disappear_from_dom(self.NO_POSITIONS_MESSAGE, timeout)
        except Exception:
            pass
        self.wait_for(lambda d: len(self.get_job_list()) > 0)
    
    def select_location_filter(self, location: str) -> None:
        self.select_by_visible_text(self.LOCATION_FILTER, location)
    
    def select_department_filter(self, department: str) -> None:
        self.select_by_visible_text(self.DEPARTMENT_FILTER, department)
    
    def get_job_list(self) -> list:
        return self.find_elements(self.JOB_LIST)
    
    def get_all_job_details(self) -> list[dict]:
        jobs = []
        job_list = self.get_job_list()
        
        for job in job_list:
            try:
                position = job.find_element(*self.JOB_POSITION_TITLE).text.strip()
                department = job.find_element(*self.JOB_POSITION_DEPARTMENT).text.strip()
                location = job.find_element(*self.JOB_POSITION_LOCATION).text.strip()
                
                jobs.append({
                    "position": position,
                    "department": department,
                    "location": location,
                    "element": job
                })
            except Exception:
                continue
        
        return jobs
    
    def click_view_role_for_job(self, job_element) -> None:
        view_role_button = job_element.find_element(*self.VIEW_ROLE_BUTTON)
        view_role_button.click()
    
    LEVER_POSTING_TITLE = (By.CSS_SELECTOR, ".posting-headline h2")
    
    def is_lever_application_page(self) -> bool:
        current_url = self.get_current_url()
        return "lever.co" in current_url or "jobs.lever.co" in current_url
    
    def get_lever_job_title(self) -> str:
        return self.find_element(self.LEVER_POSTING_TITLE).text.strip()