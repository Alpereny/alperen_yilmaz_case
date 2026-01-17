# 🖥️ UI Test Automation - Insider Website

This directory contains Selenium-based UI test automation for the [Insider](https://insiderone.com/) website using the Page Object Model design pattern.

## 📋 Overview

The UI tests validate critical user journeys on the Insider website, including home page verification and QA careers job filtering functionality.

## 🏗️ Project Structure

```
ui-test/
├── config.py           # Configuration management (pyproject.toml + env vars)
├── conftest.py         # Pytest fixtures and hooks
├── pages/              # Page Object Model classes
│   ├── base_page.py    # Base page with common methods
│   ├── home_page.py    # Home page object
│   └── qa_careers_page.py  # QA Careers page object
├── tests/              # Test cases
│   ├── conftest.py     # Test-specific fixtures
│   ├── home_test.py    # Home page tests
│   └── qa_careers_test.py  # QA careers tests
├── reports/            # Test artifacts
│   └── screenshots/    # Failure screenshots
├── pyproject.toml      # Project configuration
├── requirements.txt    # Python dependencies
└── Dockerfile          # Docker configuration
```

## 🎯 Test Scenarios

### Home Page Tests (`home_test.py`)

| Test Case | Description |
|-----------|-------------|
| `test_home_page_opened` | Verify home page loads with correct URL and title |
| `test_element_displayed` | Verify all main page blocks are visible (parametrized) |

**Page Blocks Verified:**
- Header, Navigation, Logo
- Social Proof, Core Differentiators, Capabilities
- Insider One AI, Channels, Case Study
- Analyst, Integrations, Resources
- Call to Action, Footer

### QA Careers Tests (`qa_careers_test.py`)

| Test Case | Description |
|-----------|-------------|
| `test_qa_jobs_filter_and_verify` | Filter jobs by Istanbul/QA and verify all listings match criteria |
| `test_view_role_redirects_to_lever` | Verify "View Role" opens correct Lever application page |

**Test Flow:**
1. Navigate to QA Careers page
2. Click "See all QA jobs" button
3. Filter by Location: "Istanbul, Turkiye"
4. Filter by Department: "Quality Assurance"
5. Verify each job listing contains correct position, department, and location
6. Click "View Role" and verify redirect to Lever with matching job title

## 🛠 Technology Stack

- **Python 3.11+**
- **Selenium WebDriver** - Browser automation
- **Pytest** - Test framework
- **Allure-Pytest** - Test reporting
- **Page Object Model** - Design pattern

## 🚀 Key Features

### 🌐 Cross-Browser Support

Run tests on Chrome or Firefox:

```bash
# Chrome (default)
UI_TEST_DRIVER_TYPE=chrome pytest

# Firefox
UI_TEST_DRIVER_TYPE=firefox pytest
```

### 🕸️ Selenium Grid Support

Run tests on remote Selenium Grid:

```bash
SELENIUM_GRID_URL=http://localhost:4444/wd/hub pytest
```

### 📸 Screenshot on Failure

Automatic screenshot capture when tests fail, saved to `reports/screenshots/` and attached to Allure report.

### 🎥 Video Recording

When using Selenium Grid, test sessions are recorded and embedded in Allure reports.

### ⚙️ Flexible Configuration

Configure via `pyproject.toml` or environment variables (env vars take precedence).

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- Chrome or Firefox browser
- ChromeDriver or GeckoDriver (matching browser version)

### Installation

1. Navigate to the ui-test directory:

```bash
cd ui-test
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Unix/macOS
# or
venv\Scripts\activate     # On Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

### Running Tests

#### Basic Execution

```bash
pytest
```

#### With Verbose Output

```bash
pytest -v
```

#### Run Specific Test File

```bash
pytest tests/home_test.py -v
pytest tests/qa_careers_test.py -v
```

#### With Allure Report

```bash
pytest --alluredir=allure-results
allure serve allure-results
```

#### Headless Mode

```bash
UI_TEST_HEADLESS=true pytest
```

## 🐳 Docker Execution

Run tests using Docker with Selenium Grid:

```bash
# From project root - start infrastructure first
./run-tests.sh --start-infra

# Run UI tests
./run-tests.sh --ui --browser chrome

# Or with Docker Compose directly
docker compose --profile test up ui-test --build
```

Watch tests in real-time via noVNC:
- Chrome: http://localhost:7900
- Firefox: http://localhost:7901

## 🔧 Configuration

### pyproject.toml

```toml
[tool.ui-test-config]
driver_type = "chrome"
base_url = "https://insiderone.com/"
qa_careers_url = "https://insiderone.com/careers/quality-assurance/"
headless = false
implicit_wait_timeout = 30
element_wait_timeout = 15
screenshot_dir = "reports/screenshots"
screenshot_on_failure = true
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `UI_TEST_DRIVER_TYPE` | Browser type (chrome/firefox) | chrome |
| `UI_TEST_BASE_URL` | Base URL for tests | https://insiderone.com/ |
| `UI_TEST_HEADLESS` | Run in headless mode | false |
| `SELENIUM_GRID_URL` | Selenium Grid hub URL | None (local) |
| `MINIO_ENDPOINT` | MinIO URL for video links | http://localhost:9000 |

## 🏛️ Page Object Model

### Base Page

All page objects extend `BasePage` which provides common methods:

```python
class BasePage:
    def find_element(self, locator)
    def find_elements(self, locator)
    def wait_for(self, condition, timeout)
    def scroll_to(self, locator)
    def is_displayed(self, locator)
    def go_to_url(self, url)
    # ... and more
```

### Page Objects

```python
# Home Page
home_page = HomePage(driver)
home_page.get_element_locator("Header")
home_page.is_displayed(locator)

# QA Careers Page
qa_page = QACareersPage(driver)
qa_page.go_to_qa_careers()
qa_page.click_see_all_qa_jobs_button()
qa_page.select_location_filter("Istanbul, Turkiye")
qa_page.select_department_filter("Quality Assurance")
jobs = qa_page.get_all_job_details()
```

## 📊 Test Reports

### Allure Report Features

- Test execution timeline
- Screenshots on failure (automatically attached)
- Video recordings (when using Selenium Grid)
- Detailed step logging
- Test categorization by feature/story

### Access Reports

Via Docker infrastructure:
- Allure UI: http://localhost:5252
- Direct Report: http://localhost:5050/allure-docker-service/projects/default/reports/latest/index.html

## 📝 Dependencies

```
pytest==8.4.1
selenium==4.35.0
allure-pytest>=2.13.5
```

## 🎥 Demo

Tests running on Selenium Grid with video recording:

![Selenium Grid Demo](../images/seleniumgriddemo1.gif)

Test results with embedded video in Allure:

![Allure Report with Video](../images/allurereportvideo.gif)
