from fastapi import APIRouter
from .profile import company_profile_router
from .orders import order_router

company_router = APIRouter(prefix="/company")

company_router.include_router(company_profile_router)
company_router.include_router(order_router)
