from typing import Optional
from pydantic import BaseModel, Field


class Category(BaseModel):
    id: Optional[int] = Field(default=None)
    name: Optional[str] = Field(default=None)
