from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.api.services.utilities.hash_password import get_password_hash
from src.orm.repositories.user import UserRepository
from src.orm.repositories.driver import DriverRepository
from src.orm.repositories.company import CompanyRepository
from src.schemas.requests.auth import DriverCreate, CompanyCreate
from src.orm.models.user import User
from src.orm.database import with_db

@with_db
def register_driver(driver_data: DriverCreate, db: Session = None) -> User:
    
    user_repo = UserRepository(db)
    driver_repo = DriverRepository(db)
    
    if user_repo.get_by_email(driver_data.email):
        raise HTTPException(status_code=400, detail='Этот email уже занят')
    
    user = user_repo.create(driver_data.email, get_password_hash(driver_data.password), 'driver')
    driver_repo.create(user.id, driver_data.full_name, driver_data.phone, driver_data.transport_type)
    db.commit()
    db.refresh(user)
    return user


@with_db
def register_company(company_data: CompanyCreate, db: Session = None) -> User:
    
    user_repo = UserRepository(db)
    company_repo = CompanyRepository(db)

    if user_repo.get_by_email(company_data.email):
        raise HTTPException(status_code=400, detail="Этот email уже занят")

    user = user_repo.create(company_data.email, get_password_hash(company_data.password), "company")
    company_repo.create(user.id, company_data.company_name, company_data.ttn, company_data.phone, company_data.rep_full_name)
    db.commit()
    db.refresh(user)
    return user