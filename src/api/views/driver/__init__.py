from fastapi import APIRouter
from .profile import driver_profile_router
from .vehicles import vehicle_router

driver_router = APIRouter()

driver_router.include_router(driver_profile_router)
driver_router.include_router(vehicle_router)
