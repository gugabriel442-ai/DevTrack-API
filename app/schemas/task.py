
from pydantic import BaseModel, ConfigDict, Field
from typing import Literal
from datetime import datetime


class TaskCreate(BaseModel):
    title: str = Field(min_length=2, max_length=100)
    description: str | None = None
    due_date: datetime | None = None


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=100)
    description: str | None = None
    status: Literal["pending", "in_progress", "completed"] | None = None
    due_date: datetime | None = None


class TaskResponse(BaseModel):
    id: int
    project_id: int
    title: str
    description: str | None
    status: str
    due_date: datetime | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
