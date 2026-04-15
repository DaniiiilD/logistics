from fastapi import APIRouter, Depends
from src.api.middlewares.session import in_session
from src.api.handlers.user import UserService
from src.api.middlewares.jwt_token import RoleChecker
from src.schemas.requests.users import DriverUpdate
from src.schemas.responses.users import DriverProfileResponse

driver_profile_router = APIRouter(prefix="/profile", tags=["Профиль водителя"])


@driver_profile_router.get("", response_model=DriverProfileResponse)
@in_session
async def get_driver_me(
    user_id: int = Depends(RoleChecker(["driver"])), service: UserService = Depends()
):
    return await service.get_driver_profile(user_id)


@driver_profile_router.patch("", response_model=DriverProfileResponse)
@in_session
async def update_driver_me(
    data: DriverUpdate,
    user_id: int = Depends(RoleChecker(["driver"])),
    service: UserService = Depends(),
):
    return await service.update_driver_profile(user_id, data)
