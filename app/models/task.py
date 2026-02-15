from datetime import datetime
from uuid import uuid4
from pydantic import BaseModel, Field
from typing import Literal
from sqlalchemy import Column, String, DateTime, Boolean

from app.core.database import Base

class UpdateTaskStatus(BaseModel):
    completed: bool

class TaskDB(Base):
    __tablename__ = "tasks"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    title = Column(String(200), nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    completed_at = Column(DateTime, nullable=True)

class TaskCreate(BaseModel):
    title: str = Field(
        default=...,
        min_length=1,
        max_length=200,
    )
    description: str | None

class Task(TaskCreate):
    id: str
    completed: bool
    created_at: datetime
    completed_at: datetime | None

    class Config:
        from_attributes = True

