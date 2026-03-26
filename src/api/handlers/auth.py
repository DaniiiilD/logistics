from fastapi import HTTPException
from src.api.services.utilities.hash_password import get_password_hash
from src.orm.repositories.user import UserRepository
from src.orm.repositories.driver import DriverRepository
from src.orm.repositories.company import CompanyRepository
from src.schemas.requests.auth import DriverCreate, CompanyCreate
from src.schemas.responses.auth import UserResponse
from src.orm.models.user import User
from src.orm.models.company import Company
from src.orm.models.driver import Driver

async def register_driver(driver_data: DriverCreate,
                          user_repo: UserRepository,
                          driver_repo: DriverRepository) -> UserResponse:
    
    
    if await user_repo.get_by_email(driver_data.email):
        raise HTTPException(status_code=400, detail='Этот email уже занят')
    
    new_user = User(
        email = driver_data.email,
        hashed_password=get_password_hash(driver_data.password),
        role="driver"
    )
    user =  await user_repo.create(new_user)
    
    new_driver = Driver(
        user_id=user.id,
        full_name=driver_data.full_name,
        phone=driver_data.phone,
        transport_type = driver_data.transport_type
    )
    
    await driver_repo.create(new_driver)
  
    return UserResponse.model_validate(user)


async def register_company(company_data: CompanyCreate,
                           user_repo: UserRepository,
                           company_repo: CompanyRepository) -> UserResponse:

    if await user_repo.get_by_email(company_data.email):
        raise HTTPException(status_code=400, detail="Этот email уже занят")

    new_user = User(
        email = company_data.email,
        hashed_password=get_password_hash(company_data.password),
        role="company"
    )
    user = await user_repo.create(new_user)
    
    
    new_company = Company(
        user_id = user.id,
        company_name = company_data.company_name,
        ttn = company_data.ttn,
        phone = company_data.phone,
        rep_full_name = company_data.rep_full_name
    )
    await company_repo.create(new_company)
    
    return UserResponse.model_validate(user)