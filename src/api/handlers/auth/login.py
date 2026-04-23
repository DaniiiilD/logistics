from fastapi import HTTPException, Response, Depends
from src.api.services.utilities.hash_password import verify_password
from src.orm.repositories.user import UserRepository
from src.schemas.responses.auth import LoginResponse
from src.api.middlewares.jwt_token import create_access_token


class LoginService:
    def __init__(self, user_repo: UserRepository = Depends()):
        self.user_repo = user_repo

    async def login_user(
        self, username: str, password: str, response: Response
    ) -> LoginResponse:

        user = await self.user_repo.get_by_email(username)
        if not user:
            raise HTTPException(status_code=401, detail="Неверный email или пароль")

        if not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="неверный email или пароль")

        access_token = create_access_token(
            data={"sub": str(user.id), "role": user.role}
        )

        response.set_cookie(
            key="access_token", value=access_token, httponly=True, max_age=30 * 60
        )

        return LoginResponse(id=user.id, email=user.email, role=user.role)
