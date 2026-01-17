from typing import Optional
from pydantic import BaseModel, Field


class ApiResponse(BaseModel):
    code: Optional[int] = Field(default=None)
    type: Optional[str] = Field(default=None)
    message: Optional[str] = Field(default=None)
