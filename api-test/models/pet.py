from typing import Optional
from pydantic import BaseModel, Field

from .category import Category
from .tag import Tag
from .enums import PetStatus


class Pet(BaseModel):
    id: Optional[int] = Field(default=None)
    category: Optional[Category] = Field(default=None)
    name: Optional[str] = Field(default=None)
    photoUrls: list[str] = Field(default_factory=list, alias="photoUrls")
    tags: Optional[list[Tag]] = Field(default=None)
    status: Optional[PetStatus] = Field(default=None)

    model_config = {
        "populate_by_name": True,
        "use_enum_values": True,
    }
