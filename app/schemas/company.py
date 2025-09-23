from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CompanyBase(BaseModel):
    name: str
    description: Optional[str] = None
    mode: Optional[str] = None
    rating: Optional[int] = None


class CompanyCreate(CompanyBase):
    pass


class Company(CompanyBase):
    id: int

    class Config:
        from_attributes = True
