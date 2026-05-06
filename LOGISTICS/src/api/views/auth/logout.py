from fastapi import APIRouter, Response

logout_router = APIRouter(prefix="/logout", tags=["Выход из профиля"])


@logout_router.post("")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Вы умпешно вышли из системы"}
