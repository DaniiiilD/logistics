from fastapi import APIRouter

from src.api.views.auth import auth_router
from src.api.views.driver import driver_router
from src.api.views.company import company_router
from src.api.views.vehicle import vehicle_router

api_router = APIRouter(prefix="/api")

api_router.include_router(auth_router)
api_router.include_router(driver_router)
api_router.include_router(company_router)
api_router.include_router(vehicle_router)
