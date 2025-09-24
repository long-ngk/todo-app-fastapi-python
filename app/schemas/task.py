from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from app.enums import TaskStatus


class TaskBase(BaseModel):
    summary: str
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[str] = None


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
