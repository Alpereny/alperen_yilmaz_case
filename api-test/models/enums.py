from enum import Enum


class PetStatus(str, Enum):
    available = "available"
    pending = "pending"
    sold = "sold"
