from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from src.api.services.utilities.hash_password import verify_password
from src.orm.repositories.user import UserRepository
from src.schemas.responses.auth import LoginResponse
from src.orm.models.user import User
from src.api.dependencies import in_session

@in_session
async def login_user(username: str, password: str, session: AsyncSession = None) -> LoginResponse:
    user_repo = UserRepository(session)
    user = await user_repo.get_by_email(username)
    if not user:
        raise HTTPException(status_code=401, detail = "Неверный email или пароль")
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail = 'неверный email или пароль')
    return LoginResponse(id=user.id, email=user.email, role=user.role)
