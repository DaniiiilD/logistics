from fastapi import APIRouter, Depends, Response
from src.api.middlewares.session import in_session
from src.api.handlers.user import UserService
from src.api.middlewares.jwt_token import get_user_if_from_token
from src.schemas.requests.users import ProfileUpdate
from src.schemas.responses.users import ProfileResponse

profile_router = APIRouter(prefix="/profile", tags=["Управление профилем"])


@profile_router.get("/me", response_model=ProfileResponse)
@in_session
async def get_my_profile(
    user_id: int = Depends(get_user_if_from_token), service: UserService = Depends()
):

    return await service.get_profile(user_id)


@profile_router.patch("/me", response_model=ProfileResponse)
@in_session
async def update_my_profile(
    data: ProfileUpdate,
    user_id: int = Depends(get_user_if_from_token),
    service: UserService = Depends(),
):
    return await service.update_profile(user_id, data)


@profile_router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Вы успешно вышли из системы"}
