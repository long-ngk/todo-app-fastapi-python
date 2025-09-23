from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CompanyBase(BaseModel):
    name: str
    description: Optional[str] = None


class CompanyCreate(CompanyBase):
    pass


class Company(CompanyBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
