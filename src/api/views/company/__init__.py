from fastapi import APIRouter
from .profile import company_profile_router

company_router = APIRouter()

company_router.include_router(company_profile_router)
