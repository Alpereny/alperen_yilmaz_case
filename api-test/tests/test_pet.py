import http.client
import pytest
from faker import Faker
from models.pet import Pet
from models.category import Category
from models.tag import Tag
from models.enums import PetStatus
from service.pet_service import PetService


class TestGetPet:
    @pytest.fixture
    def existing_pet(self, pet_service: PetService):
        faker = Faker()
        pet = Pet(
            id=faker.random_int(min=100000, max=999999),
            name=faker.first_name(),
            photoUrls=[faker.image_url()],
            status=PetStatus.available,
        )
        pet_service.create_pet(pet)
        yield pet
        pet_service.delete_pet_by_id(pet.id)

    def test_get_pet_by_id_returns_ok(self, pet_service: PetService, existing_pet: Pet):
        response = pet_service.get_pet_by_id(existing_pet.id)
        assert (
            response.status_code == http.client.OK
        ), f"Expected 200, got {response.status_code}"

    def test_get_pet_by_id_returns_correct_data(self, pet_service: PetService, existing_pet: Pet):
        response = pet_service.get_pet_by_id(existing_pet.id)
        fetched = Pet.model_validate(response.json())
        assert fetched.id == existing_pet.id
        assert fetched.name == existing_pet.name

    def test_get_pet_with_invalid_id_returns_not_found(self, pet_service: PetService):
        response = pet_service.get_pet_by_id("invalid_string")
        assert response.status_code == http.client.NOT_FOUND

    def test_get_pet_with_nonexistent_id_returns_404(self, pet_service: PetService):
        response = pet_service.get_pet_by_id(999999999)
        assert response.status_code == http.client.NOT_FOUND
        assert response.json() == {
            "code": 1,
            "type": "error",
            "message": "Pet not found",
        }


class TestCreatePet:
    def test_create_pet_returns_ok(self, pet_service: PetService):
        faker = Faker()
        pet = Pet(
            id=faker.random_int(min=100000, max=999999),
            name=faker.first_name(),
            photoUrls=[faker.image_url()],
            status=PetStatus.available,
        )
        response = pet_service.create_pet(pet)
        assert response.status_code == http.client.OK
        pet_service.delete_pet_by_id(pet.id)

    def test_create_pet_response_matches_request(self, pet_service: PetService):
        faker = Faker()
        pet = Pet(
            id=faker.random_int(min=100000, max=999999),
            category=Category(id=faker.random_int(min=1, max=999), name=faker.word()),
            name=faker.first_name(),
            photoUrls=[faker.image_url()],
            tags=[Tag(id=faker.random_int(min=1, max=999), name=faker.word())],
            status=PetStatus.pending,
        )
        response = pet_service.create_pet(pet)
        created = Pet.model_validate(response.json())
        assert created == pet
        pet_service.delete_pet_by_id(pet.id)

    def test_created_pet_can_be_retrieved(self, pet_service: PetService):
        faker = Faker()
        pet = Pet(
            id=faker.random_int(min=100000, max=999999),
            name=faker.first_name(),
            photoUrls=[faker.image_url()],
            status=PetStatus.sold,
        )
        pet_service.create_pet(pet)
        
        get_response = pet_service.get_pet_by_id(pet.id)
        fetched = Pet.model_validate(get_response.json())
        assert fetched.id == pet.id
        assert fetched.name == pet.name
        
        pet_service.delete_pet_by_id(pet.id)

    def test_create_pet_with_empty_body_returns_ok(self, pet_service: PetService):
        response = pet_service.create_pet({})
        assert response.status_code == http.client.OK

    def test_create_pet_with_invalid_id_type_returns_500(self, pet_service: PetService):
        faker = Faker()
        data = {
            "id": "not_a_number",
            "name": faker.first_name(),
            "photoUrls": [faker.image_url()],
        }
        response = pet_service.create_pet(data)
        assert response.status_code == http.client.INTERNAL_SERVER_ERROR


class TestUpdatePet:
    @pytest.fixture
    def pet_to_update(self, pet_service: PetService):
        faker = Faker()
        pet = Pet(
            id=faker.random_int(min=100000, max=999999),
            name=faker.first_name(),
            photoUrls=[faker.image_url()],
            status=PetStatus.available,
        )
        pet_service.create_pet(pet)
        yield pet
        pet_service.delete_pet_by_id(pet.id)

    def test_update_pet_returns_ok(self, pet_service: PetService, pet_to_update: Pet):
        faker = Faker()
        updated = Pet(
            id=pet_to_update.id,
            name=faker.first_name(),
            photoUrls=[faker.image_url()],
            status=PetStatus.sold,
        )
        response = pet_service.update_pet(updated)
        assert response.status_code == http.client.OK

    def test_update_pet_response_matches_request(self, pet_service: PetService, pet_to_update: Pet):
        faker = Faker()
        updated = Pet(
            id=pet_to_update.id,
            name=faker.first_name(),
            category=Category(id=faker.random_int(min=1, max=999), name=faker.word()),
            photoUrls=[faker.image_url()],
            tags=[Tag(id=faker.random_int(min=1, max=999), name=faker.word())],
            status=PetStatus.pending,
        )
        response = pet_service.update_pet(updated)
        result = Pet.model_validate(response.json())
        assert result == updated

    def test_updated_pet_persists(self, pet_service: PetService, pet_to_update: Pet):
        faker = Faker()
        new_name = faker.first_name()
        updated = Pet(
            id=pet_to_update.id,
            name=new_name,
            photoUrls=[faker.image_url()],
            status=PetStatus.sold,
        )
        pet_service.update_pet(updated)
        
        get_response = pet_service.get_pet_by_id(pet_to_update.id)
        fetched = Pet.model_validate(get_response.json())
        assert fetched.name == new_name
        assert fetched.status == PetStatus.sold


class TestUpdatePetById:
    @pytest.fixture
    def pet_for_form_update(self, pet_service: PetService):
        faker = Faker()
        pet = Pet(
            id=faker.random_int(min=100000, max=999999),
            name=faker.first_name(),
            photoUrls=[faker.image_url()],
            status=PetStatus.available,
        )
        pet_service.create_pet(pet)
        yield pet
        pet_service.delete_pet_by_id(pet.id)

    def test_update_pet_by_id_returns_ok(self, pet_service: PetService, pet_for_form_update: Pet):
        faker = Faker()
        update_data = {"name": faker.first_name(), "status": PetStatus.pending}
        response = pet_service.update_pet_by_id(pet_for_form_update.id, update_data)
        assert response.status_code == http.client.OK

    def test_update_pet_by_id_persists(self, pet_service: PetService, pet_for_form_update: Pet):
        faker = Faker()
        new_name = faker.first_name()
        update_data = {"name": new_name, "status": PetStatus.sold}
        pet_service.update_pet_by_id(pet_for_form_update.id, update_data)
        
        get_response = pet_service.get_pet_by_id(pet_for_form_update.id)
        fetched = Pet.model_validate(get_response.json())
        assert fetched.name == new_name
        assert fetched.status == PetStatus.sold


class TestDeletePet:
    def test_delete_pet_returns_ok(self, pet_service: PetService):
        faker = Faker()
        pet = Pet(
            id=faker.random_int(min=100000, max=999999),
            name=faker.first_name(),
            photoUrls=[faker.image_url()],
            status=PetStatus.available,
        )
        pet_service.create_pet(pet)
        
        response = pet_service.delete_pet_by_id(pet.id)
        assert response.status_code == http.client.OK

    def test_deleted_pet_cannot_be_found(self, pet_service: PetService):
        faker = Faker()
        pet = Pet(
            id=faker.random_int(min=100000, max=999999),
            name=faker.first_name(),
            photoUrls=[faker.image_url()],
            status=PetStatus.available,
        )
        pet_service.create_pet(pet)
        pet_service.delete_pet_by_id(pet.id)
        
        get_response = pet_service.get_pet_by_id(pet.id)
        assert get_response.status_code == http.client.NOT_FOUND

    def test_delete_nonexistent_pet_returns_404(self, pet_service: PetService):
        response = pet_service.delete_pet_by_id(999999999)
        assert response.status_code == http.client.NOT_FOUND
