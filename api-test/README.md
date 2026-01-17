# 🧪 API Test Automation - Petstore API

This directory contains Pytest-based API test automation for the [Petstore Swagger](https://petstore.swagger.io/) pet endpoints.

## 📋 Overview

The API tests cover CRUD operations for the Pet resource using a clean service layer architecture with Pydantic models for request/response validation.

## 🏗️ Project Structure

```
api-test/
├── config.py           # Configuration settings (base URL, timeout)
├── conftest.py         # Pytest fixtures
├── models/             # Pydantic data models
│   ├── pet.py          # Pet model
│   ├── category.py     # Category model
│   ├── tag.py          # Tag model
│   ├── enums.py        # Status enums
│   └── api_response.py # API response model
├── service/            # Service layer
│   ├── base_service.py # Base HTTP client
│   └── pet_service.py  # Pet-specific API operations
├── tests/              # Test cases
│   └── test_pet.py     # Pet endpoint tests
├── requirements.txt    # Python dependencies
└── Dockerfile          # Docker configuration
```

## 🎯 Test Coverage

### Endpoints Tested

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/pet/{petId}` | Retrieve pet by ID |
| `POST` | `/pet` | Create new pet |
| `PUT` | `/pet` | Update existing pet |
| `POST` | `/pet/{petId}` | Update pet with form data |
| `DELETE` | `/pet/{petId}` | Delete pet |

### Test Cases

#### GET Pet Tests
- ✅ Get pet by valid ID returns 200 OK
- ✅ Get pet returns correct data
- ✅ Get pet with invalid ID returns 404 Not Found
- ✅ Get pet with nonexistent ID returns 404

#### POST Pet (Create) Tests
- ✅ Create pet returns 200 OK
- ✅ Created pet response matches request
- ✅ Created pet can be retrieved
- ✅ Create pet with empty body returns 200
- ✅ Create pet with invalid ID type returns 500

#### PUT Pet (Update) Tests
- ✅ Update pet returns 200 OK
- ✅ Updated pet response matches request
- ✅ Updated pet persists changes

#### POST Pet by ID (Form Update) Tests
- ✅ Update pet by ID returns 200 OK
- ✅ Form update persists changes

#### DELETE Pet Tests
- ✅ Delete pet returns 200 OK
- ✅ Deleted pet cannot be found
- ✅ Delete nonexistent pet returns 404

## 🛠 Technology Stack

- **Python 3.10+**
- **Pytest** - Test framework
- **Requests** - HTTP client
- **Pydantic** - Data validation and modeling
- **Faker** - Test data generation
- **Allure-Pytest** - Test reporting

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Installation

1. Navigate to the api-test directory:

```bash
cd api-test
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

#### Run Specific Test Class

```bash
pytest tests/test_pet.py::TestGetPet -v
pytest tests/test_pet.py::TestCreatePet -v
pytest tests/test_pet.py::TestUpdatePet -v
pytest tests/test_pet.py::TestDeletePet -v
```

#### With Allure Report

```bash
pytest --alluredir=allure-results
allure serve allure-results
```

## 🐳 Docker Execution

Run tests using Docker:

```bash
# Build and run from project root
docker compose --profile test up api-test --build

# Or build standalone
cd api-test
docker build -t api-test .
docker run api-test
```

## 🔧 Configuration

Edit `config.py` to modify settings:

```python
BASE_URL = "https://petstore.swagger.io/v2"  # API base URL
TIMEOUT = 30                                   # Request timeout in seconds
```

## 🏛️ Architecture

### Service Layer Pattern

The tests use a service layer pattern for clean API abstraction:

```python
# Using PetService
pet_service = PetService(BASE_URL, TIMEOUT)

# Create a pet
pet = Pet(id=123, name="Buddy", photoUrls=["http://example.com/photo.jpg"])
response = pet_service.create_pet(pet)

# Get a pet
response = pet_service.get_pet_by_id(123)
```

### Pydantic Models

Request/response data is validated using Pydantic models:

```python
class Pet(BaseModel):
    id: int | None = None
    category: Category | None = None
    name: str
    photoUrls: list[str]
    tags: list[Tag] | None = None
    status: PetStatus | None = None
```

### Test Fixtures

Tests use pytest fixtures for setup/teardown:

```python
@pytest.fixture
def existing_pet(self, pet_service: PetService):
    # Create pet before test
    pet = Pet(id=faker.random_int(), name=faker.first_name(), ...)
    pet_service.create_pet(pet)
    yield pet
    # Cleanup after test
    pet_service.delete_pet_by_id(pet.id)
```

## 📊 Allure Report

Tests include Allure annotations for comprehensive reporting. After running tests with `--alluredir`, generate the report:

```bash
allure serve allure-results
```

Or view via Docker infrastructure:
- Allure UI: http://localhost:5252

## 📝 Dependencies

```
requests>=2.32.5
pytest>=9.0.2
pydantic>=2.12.5
faker>=40.1.2
allure-pytest>=2.15.3
```
