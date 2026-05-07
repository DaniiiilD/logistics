from fastapi import APIRouter, Depends
from src.api.middlewares.session import in_session
from src.api.handlers.user import UserService
from src.api.middlewares.jwt_token import RoleChecker
from src.schemas.requests.users import DriverUpdate
from src.schemas.responses.users import DriverProfileResponse
from src.core.constants import Role

router = APIRouter(prefix="/profile", tags=["Профиль водителя"])


@router.get("", response_model=DriverProfileResponse)
@in_session
async def get_driver_me(
    user_id: int = Depends(RoleChecker([Role.DRIVER])), service: UserService = Depends()
):
    return await service.get_driver_profile(user_id)


@router.patch("", response_model=DriverProfileResponse)
@in_session
async def update_driver_me(
    data: DriverUpdate,
    user_id: int = Depends(RoleChecker([Role.DRIVER])),
    service: UserService = Depends(),
):
    return await service.update_driver_profile(user_id, data)
