from fastapi import APIRouter, Depends, Response
from src.schemas.responses.auth import LoginResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from src.api.middlewares.session import in_session
from src.api.handlers.login import LoginService

security = HTTPBasic()
login_router = APIRouter(prefix="/login", tags=["Вход"])


@login_router.post("", response_model=LoginResponse)
@in_session
async def login(
    response: Response,
    credentials: HTTPBasicCredentials = Depends(security),
    login_service: LoginService = Depends(),
):

    return await login_service.login_user(
        credentials.username, credentials.password, response
    )
