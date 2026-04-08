from fastapi import APIRouter, Depends, Response
from src.api.middlewares.session import in_session
from src.api.handlers.user import UserService
from src.api.middlewares.jwt_token import require_company, require_driver
from src.schemas.requests.users import DriverUpdate, CompanyUpdate
from src.schemas.responses.users import DriverProfileResponse, CompanyProfileResponse

common_profile_router = APIRouter(prefix="/profile", tags=["Общий профиль"])


@common_profile_router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Вы умпешно вышли из системы"}


driver_profile_router = APIRouter(prefix="/profile/driver", tags=["Профиль водителя"])


@driver_profile_router.get("/me", response_model=DriverProfileResponse)
@in_session
async def get_driver_me(
    user_id: int = Depends(require_driver), service: UserService = Depends()
):
    return await service.get_driver_profile(user_id)


@driver_profile_router.patch("/me", response_model=DriverProfileResponse)
@in_session
async def update_driver_me(
    data: DriverUpdate,
    user_id: int = Depends(require_driver),
    service: UserService = Depends(),
):
    return await service.update_driver_profile(user_id, data)


company_profile_router = APIRouter(prefix="/profile/company", tags=["Профиль компании"])


@company_profile_router.get("/me", response_model=CompanyProfileResponse)
@in_session
async def get_company_me(
    user_id: int = Depends(require_company), service: UserService = Depends()
):
    return await service.get_company_profile(user_id)


@company_profile_router.patch("/me", response_model=CompanyProfileResponse)
@in_session
async def update_company_me(
    data: CompanyUpdate,
    user_id: int = Depends(require_company),
    service: UserService = Depends(),
):
    return await service.update_company_profile(user_id, data)
