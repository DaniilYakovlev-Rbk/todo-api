from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field
from typing import Literal

class TaskCreate(BaseModel):
    title: str = Field(
        default=...,
        min_length=1,
        max_length=200,
    )
    description: str | None

class Task(TaskCreate):
    id: str
    status: Literal["active", "completed"]
    created_at: datetime
    completed_at: datetime | None

    @classmethod
    def create(cls, title: str, description: str | None) -> "Task":
        now = datetime.now()

        return cls(
            id=str(uuid4()),
            title=title,
            description=description,
            status="active",
            created_at=now,
            completed_at=None
        )

    def complete(self) -> None:
        self.status = "completed"
        self.completed_at = datetime.now()

    def uncomplete(self) -> None:
        self.status = "active"
        self.completed_at = None

class UpdateTaskStatus(BaseModel):
    status: Literal["active", "completed"]