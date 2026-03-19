from fastapi import APIRouter
from src.schemas.responses.auth import UserResponse
from src.schemas.requests.auth import DriverCreate, CompanyCreate
from src.api.handlers.auth import register_driver, register_company


auth_router = APIRouter(prefix='/auth', tags=['Регистрация'])


@auth_router.post('/driver', response_model=UserResponse)
def driver(driver_data: DriverCreate):
    return register_driver(driver_data)
    
@auth_router.post('/company', response_model=UserResponse)
def company(company_data: CompanyCreate):
    return register_company(company_data)