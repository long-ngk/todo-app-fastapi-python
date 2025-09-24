from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models.models import Company, User
from app.schemas.company import Company as CompanySchema
from app.schemas.company import CompanyCreate

router = APIRouter()


@router.post("/companies/", response_model=CompanySchema)
def create_company(
    company: CompanyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_company = Company(**company.model_dump())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company


@router.get("/companies/", response_model=List[CompanySchema])
def read_companies(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not getattr(current_user, 'is_admin', False):
        raise HTTPException(status_code=403, detail="Only admin can view all companies")
    companies = db.query(Company).offset(skip).limit(limit).all()
    return companies


@router.get("/companies/{company_id}", response_model=CompanySchema)
def read_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not getattr(current_user, 'is_admin', False) and getattr(current_user, 'company_id') != company_id:
        raise HTTPException(status_code=403, detail="You can only view your own company")
    company = db.query(Company).filter(Company.id == company_id).first()
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return company
