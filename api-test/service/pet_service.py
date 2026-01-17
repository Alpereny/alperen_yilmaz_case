from .base_service import BaseService
from models.pet import Pet


class PetService(BaseService):
    PET_PATH = "/pet"

    def __init__(self, base_url: str, timeout: int = 30):
        super().__init__(base_url, timeout)

    def create_pet(self, pet_data: Pet | dict):
        return self.post(self.PET_PATH, pet_data)

    def get_pet_by_id(self, pet_id: int | str):
        return self.get(f"{self.PET_PATH}/{pet_id}")

    def update_pet(self, pet_data: Pet | dict):
        return self.put(self.PET_PATH, pet_data)

    def update_pet_by_id(self, pet_id: int, data: dict):
        return self.post_form(f"{self.PET_PATH}/{pet_id}", data)

    def delete_pet_by_id(self, pet_id: int):
        return self.delete(f"{self.PET_PATH}/{pet_id}")

    def find_by_status(self, status: str | list[str]):
        params = {"status": status if isinstance(status, list) else [status]}
        return self.get(f"{self.PET_PATH}/findByStatus", params=params)

    def find_by_tags(self, tags: list[str]):
        return self.get(f"{self.PET_PATH}/findByTags", params={"tags": tags})
