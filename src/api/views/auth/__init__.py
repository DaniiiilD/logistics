from fastapi import APIRouter
from src.api.views.auth.auth import auth_router
from src.api.views.auth.login import login_router
from src.api.views.user_profile import (
    common_profile_router,
    company_profile_router,
    driver_profile_router,
)
from src.api.views.vehicles import vehicle_router

main_router = APIRouter()
main_router.include_router(auth_router)
main_router.include_router(login_router)
main_router.include_router(common_profile_router)
main_router.include_router(company_profile_router)
main_router.include_router(driver_profile_router)
main_router.include_router(vehicle_router)
