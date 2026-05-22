from fastapi import APIRouter, Depends
from src.schemas.responses.auth import UserResponse, TelegramLinkResponse
from src.schemas.requests.auth import DriverCreate, CompanyCreate
from src.api.middlewares.session import in_session
from src.api.handlers.auth.auth import RegistrationService
from src.api.middlewares.jwt_token import RoleChecker
from src.core.constants import Role
from src.api.handlers.user import UserService


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


@auth_router.get("/telegram-link", response_model=TelegramLinkResponse)
async def get_teleram_link(
    user_id: int = Depends(RoleChecker([Role.DRIVER])), service: UserService = Depends()
):
    token = await service.create_telegram_link_token(user_id)
    return {"link": f"https://t.me/logistics_trainee_bot?start={token}"}
