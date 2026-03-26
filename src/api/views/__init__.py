from fastapi import APIRouter
from src.api.views.auth import main_router

api_router = APIRouter(prefix="/api")

api_router.include_router(main_router)