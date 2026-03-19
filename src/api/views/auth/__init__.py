from fastapi import APIRouter
from src.api.views.auth.auth import auth_router
from src.api.views.auth.login import login_router

main_router = APIRouter()
main_router.include_router(auth_router)
main_router.include_router(login_router)