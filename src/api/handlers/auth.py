from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from src.api.services.utilities.hash_password import get_password_hash
from src.orm.repositories.user import UserRepository
from src.orm.repositories.driver import DriverRepository
from src.orm.repositories.company import CompanyRepository
from src.schemas.requests.auth import DriverCreate, CompanyCreate
from src.schemas.responses.auth import UserResponse
from src.api.dependencies import in_session

@in_session
async def register_driver(driver_data: DriverCreate, session: AsyncSession = None) -> UserResponse:
    
    user_repo = UserRepository(session)
    driver_repo = DriverRepository(session)
    
    if await user_repo.get_by_email(driver_data.email):
        raise HTTPException(status_code=400, detail='Этот email уже занят')
    
    user =  await user_repo.create(driver_data.email, get_password_hash(driver_data.password), 'driver')
    await driver_repo.create(user.id, driver_data.full_name, driver_data.phone, driver_data.transport_type)
  
    return UserResponse(id=user.id, email=user.email, role=user.role)


@in_session
async def register_company(company_data: CompanyCreate, session: AsyncSession = None) -> UserResponse:
    
    user_repo = UserRepository(session)
    company_repo = CompanyRepository(session)

    if await user_repo.get_by_email(company_data.email):
        raise HTTPException(status_code=400, detail="Этот email уже занят")

    user = await user_repo.create(company_data.email, get_password_hash(company_data.password), "company")
    await company_repo.create(user.id, company_data.company_name, company_data.ttn, company_data.phone, company_data.rep_full_name)
    
    return UserResponse(id=user.id, email=user.email, role=user.role)