from fastapi import APIRouter
from .auth import auth_router as register_router
from .login import login_router
from .logout import logout_router

auth_router = APIRouter()

auth_router.include_router(register_router)
auth_router.include_router(login_router)
auth_router.include_router(logout_router)
