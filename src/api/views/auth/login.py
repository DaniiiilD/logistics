from fastapi import APIRouter, Depends, Response
from src.schemas.responses.auth import LoginResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from src.api.handlers.login import login_user
from src.api.middlewares.session import in_session


security = HTTPBasic()
login_router = APIRouter(prefix='/login', tags=['Вход'])

@login_router.post('', response_model=LoginResponse)
@in_session
async def login(
    response: Response,
    credentials: HTTPBasicCredentials = Depends(security)
    ):
    return await  login_user(credentials.username, credentials.password, response)