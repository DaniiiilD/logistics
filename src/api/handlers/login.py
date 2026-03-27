from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Response
from src.api.services.utilities.hash_password import verify_password
from src.orm.repositories.user import UserRepository
from src.schemas.responses.auth import LoginResponse
from src.orm.models.user import User
from src.api.middlewares.jwt_token import create_access_token

async def login_user(username: str, password: str,) -> LoginResponse:
    user_repo = UserRepository()
    
    user = await user_repo.get_by_email(username)
    if not user:
        raise HTTPException(status_code=401, detail = "Неверный email или пароль")
    
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail = 'неверный email или пароль')
    
    access_token = create_access_token(data={"sub": username})
    
    Response.set_cookie(
        key="access_token",
        value="access_token",
        httponly=True,
        max_age=30*60
    )
    
    return LoginResponse(id=user.id, email=user.email, role=user.role)
