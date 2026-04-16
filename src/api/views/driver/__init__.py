from fastapi import APIRouter
from .profile import router as driver_profile_router
from .vehicles import router as vehicle_router

driver_router = APIRouter(prefix="/driver")

driver_router.include_router(driver_profile_router)
driver_router.include_router(vehicle_router)
