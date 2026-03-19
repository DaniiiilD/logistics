from fastapi import APIRouter, Depends
from src.schemas.responses.auth import LoginResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from src.api.handlers.login import login_user


security = HTTPBasic()
login_router = APIRouter(prefix='/login', tags=['Вход'])

@login_router.post('', response_model=LoginResponse)
def login(credentials: HTTPBasicCredentials = Depends(security)):
    return login_user(credentials.username, credentials.password)