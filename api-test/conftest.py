import pytest
from config import BASE_URL, TIMEOUT
from service.pet_service import PetService


@pytest.fixture(scope="session")
def pet_service() -> PetService:
    return PetService(BASE_URL, TIMEOUT)
