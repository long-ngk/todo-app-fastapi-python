from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from .company import Company


class UserBase(BaseModel):
    email: EmailStr
    username: str
    company_id: int


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    company: Optional[Company] = None

    class Config:
        from_attributes = True
