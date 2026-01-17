import time
import pytest
from pages.qa_careers_page import QACareersPage


@pytest.fixture(scope="function")
def filtered_qa_careers_page(driver):
    page = QACareersPage(driver)
    page.go_to_qa_careers()
    page.click_see_all_qa_jobs_button()
    page.wait_for_jobs_to_load(timeout=50)
    
    time.sleep(2) # for waiting for the loading location and department filters

    page.select_location_filter("Istanbul, Turkiye")
    page.select_department_filter("Quality Assurance")

    time.sleep(2) # for waiting for the filtering to complete

    return page


class TestQACareers:
    def test_qa_jobs_filter_and_verify(self, filtered_qa_careers_page: QACareersPage):
        page = filtered_qa_careers_page
        
        jobs = page.get_all_job_details()
        for job in jobs:
            assert "Quality Assurance" in job["position"], \
                f"Position '{job['position']}' does not contain 'Quality Assurance'"
            
            assert "Quality Assurance" in job["department"], \
                f"Department '{job['department']}' does not contain 'Quality Assurance'"
            
            assert "Istanbul, Turkiye" in job["location"], \
                f"Location '{job['location']}' does not contain 'Istanbul' or 'Turkey'"
    
    def test_view_role_redirects_to_lever(self, filtered_qa_careers_page: QACareersPage):
        page = filtered_qa_careers_page
        
        jobs = page.get_all_job_details()
        original_window = page.driver.current_window_handle
        
        for i, job in enumerate(jobs, 1):
            expected_title = job["position"]
            page.click_view_role_for_job(job["element"])
            time.sleep(2)
            
            all_windows = page.get_window_handles()
            
            if len(all_windows) > 1:
                for window in all_windows:
                    if window != original_window:
                        page.driver.switch_to.window(window)
                        break
                
                page.wait_for_page_load()
                
                assert page.is_lever_application_page(), \
                    f"Job {i}: Expected Lever application page, but got: {page.get_current_url()}"
                
                lever_job_title = page.get_lever_job_title()
                assert lever_job_title == expected_title, \
                    f"Job {i}: Title mismatch. Expected '{expected_title}', got '{lever_job_title}'"
                
                page.close()
                page.driver.switch_to.window(original_window)
                time.sleep(1)
