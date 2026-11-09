
from pydantic import BaseModel, ConfigDict, Field
from typing import Literal
from datetime import datetime


class ProjectCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    description: str | None = None


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    description: str | None = None
    status: Literal["active", "completed", "archived"] | None = None


class ProjectResponse(BaseModel):
    id: int
    user_id: int
    name: str
    description: str | None
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
