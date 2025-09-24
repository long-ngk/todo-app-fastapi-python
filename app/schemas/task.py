from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TaskBase(BaseModel):
    summary: str
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
