from fastapi import APIRouter
from .profile import router as driver_profile_router
from .vehicles import router as vehicle_router
from .orders import router as driver_order_router

driver_router = APIRouter(prefix="/driver")

driver_router.include_router(driver_profile_router)
driver_router.include_router(vehicle_router)
driver_router.include_router(driver_order_router)
