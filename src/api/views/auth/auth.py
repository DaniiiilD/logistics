from fastapi import APIRouter, Depends
from src.schemas.responses.auth import UserResponse
from src.schemas.requests.auth import DriverCreate, CompanyCreate
from src.api.middlewares.session import in_session
from src.api.handlers.auth import RegistrationService


auth_router = APIRouter(prefix="/auth", tags=["Регистрация"])


@auth_router.post("/driver", response_model=UserResponse)
@in_session
async def driver(
    driver_data: DriverCreate,
    registration_service: RegistrationService = Depends(),
):
    return await registration_service.register_driver(driver_data)


@auth_router.post("/company", response_model=UserResponse)
@in_session
async def company(
    company_data: CompanyCreate, registration_service: RegistrationService = Depends()
):

    return await registration_service.register_company(company_data)
