# ⚡ Load Testing - n11.com Search Module

This directory contains Locust-based load testing for the [n11.com](https://www.n11.com/) search module.

## 📋 Overview

The load test simulates user behavior when:
1. Searching for products via the header search bar
2. Viewing and navigating through search results
3. Testing edge cases with invalid search terms

## 🏗️ Project Structure

```
load-test/
├── locustfile.py       # Main Locust test file with all test scenarios
├── config.py           # Configuration settings (base URL, headers, wait times)
├── search_terms.csv    # CSV file containing product search terms
├── requirements.txt    # Python dependencies
└── README.md
```

## 🛠 Technology Stack

- **Python 3.10+**
- **Locust** - Load testing framework
- **Requests** - HTTP client (built into Locust)

## 🎯 Test Scenarios

| Scenario | Weight | Description |
|----------|--------|-------------|
| **Basic Search** | 5 | Selects a search term from CSV, performs search, validates results |
| **Pagination** | 2 | Performs search and navigates to page 2 of results |
| **Invalid Search** | 1 | Tests edge cases with invalid/special character search terms |

### Task Distribution

With the weights above, in a typical run:
- ~62.5% of tasks will be Basic Search
- ~25% of tasks will be Pagination
- ~12.5% of tasks will be Invalid Search

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Installation

1. Navigate to the load-test directory:

```bash
cd load-test
```

2. Create a virtual environment (recommended):

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

## 🏃 Running the Tests

### Web UI Mode (Recommended for Development)

Start Locust with the web interface:

```bash
locust -f locustfile.py
```

Then open [http://localhost:8089](http://localhost:8089) in your browser.

Configure the test:
- **Number of users**: Start with 1 (as per requirements)
- **Spawn rate**: 1 user per second
- **Host**: `https://www.n11.com` (pre-configured)

### Headless Mode (For CI/CD)

Run without the web interface:

```bash
# Single user, 1 minute duration
locust -f locustfile.py --headless -u 1 -r 1 -t 1m

# With HTML report
locust -f locustfile.py --headless -u 1 -r 1 -t 1m --html=report.html
```

### Command Line Options

| Option | Description | Example |
|--------|-------------|---------|
| `-u, --users` | Number of concurrent users | `-u 10` |
| `-r, --spawn-rate` | Users spawned per second | `-r 2` |
| `-t, --run-time` | Test duration | `-t 5m` |
| `--headless` | Run without web UI | `--headless` |
| `--html` | Generate HTML report | `--html=report.html` |
| `--csv` | Generate CSV statistics | `--csv=results` |

## 📊 Example Commands

```bash
# Default: 1 user for testing (as per requirements)
locust -f locustfile.py --headless -u 1 -r 1 -t 2m

# 5 users for moderate load testing
locust -f locustfile.py --headless -u 5 -r 1 -t 5m --html=report.html

# 10 users with CSV output
locust -f locustfile.py --headless -u 10 -r 2 -t 10m --csv=load_test_results
```

## 🔧 Configuration

Edit `config.py` to modify settings:

```python
# Target website
BASE_URL = "https://www.n11.com"

# Search endpoint
SEARCH_PATH = "/arama"

# Think time between requests (seconds)
MIN_WAIT_TIME = 1
MAX_WAIT_TIME = 3

# HTTP headers
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 ...",
    "Accept": "text/html,...",
    # ...
}

# Edge case search terms
INVALID_SEARCH_TERMS = [
    "xyzqwerty123",
    "nonexistingproduct",
    # ...
]
```

## 📈 Understanding Results

### Key Metrics

| Metric | Description |
|--------|-------------|
| **Requests/s** | Number of requests per second |
| **Response Time (ms)** | Time to receive response |
| **Median (50%ile)** | Half of requests are faster than this |
| **95th percentile** | 95% of requests are faster than this |
| **99th percentile** | 99% of requests are faster than this |
| **Failure Rate** | Percentage of failed requests |

### Success Criteria

A successful load test should show:
- ✅ Response times < 3 seconds for 95% of requests
- ✅ Failure rate < 1%
- ✅ No 5xx server errors

### Automatic Failure Detection

The test automatically fails (exit code 1) if the failure ratio exceeds 1%:

```python
@events.quitting.add_listener
def on_quitting(environment, **kwargs):
    if environment.stats.total.fail_ratio > 0.01:
        environment.process_exit_code = 1
```

## 📝 Customizing Search Terms

Edit `search_terms.csv` to add or modify search terms. Each line should contain one search term:

```
telefon
laptop
ayakkabı
televizyon
çanta
...
```

## 🏛️ Test Architecture

### User Behavior

Each simulated user:
1. **on_start**: Visits homepage (warmup)
2. **Tasks**: Randomly executes tasks based on weights
3. **Wait**: Pauses 1-3 seconds between tasks (think time)

### Response Validation

All search responses are validated for:
- ✅ HTTP 200 status code
- ✅ Non-empty response body
- ✅ Search query parameter in URL
- ✅ Presence of search result indicators in HTML
