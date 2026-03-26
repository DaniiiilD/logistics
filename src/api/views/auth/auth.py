from fastapi import APIRouter, Depends
from src.schemas.responses.auth import UserResponse
from src.schemas.requests.auth import DriverCreate, CompanyCreate
from src.api.handlers.auth import register_driver, register_company
from src.api.middlewares.session import in_session
from src.orm.repositories.user import UserRepository
from src.orm.repositories.driver import DriverRepository
from src.orm.repositories.company import CompanyRepository


auth_router = APIRouter(prefix='/auth', tags=['Регистрация'])


@auth_router.post('/driver', response_model=UserResponse)
@in_session
async def driver(driver_data: DriverCreate,
                 user_repo: UserRepository = Depends(),
                 driver_repo: DriverRepository = Depends()
                ):
    return await register_driver(driver_data, user_repo, driver_repo)
    
@auth_router.post('/company', response_model=UserResponse)
@in_session
async def company(company_data: CompanyCreate,
                  user_repo: UserRepository = Depends(),
                  company_repo: CompanyRepository = Depends()
                ):
    
    return await register_company(company_data, user_repo, company_repo)