from typing import Optional
from pydantic import BaseModel, Field


class Tag(BaseModel):
    id: Optional[int] = Field(default=None)
    name: Optional[str] = Field(default=None)
