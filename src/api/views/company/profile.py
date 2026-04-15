from fastapi import APIRouter, Depends
from src.api.middlewares.session import in_session
from src.api.handlers.user import UserService
from src.api.middlewares.jwt_token import RoleChecker
from src.schemas.requests.users import CompanyUpdate
from src.schemas.responses.users import CompanyProfileResponse

company_profile_router = APIRouter(prefix="/profile", tags=["Профиль компании"])


@company_profile_router.get("", response_model=CompanyProfileResponse)
@in_session
async def get_company_me(
    user_id: int = Depends(RoleChecker(["company"])), service: UserService = Depends()
):
    return await service.get_company_profile(user_id)


@company_profile_router.patch("", response_model=CompanyProfileResponse)
@in_session
async def update_company_me(
    data: CompanyUpdate,
    user_id: int = Depends(RoleChecker(["company"])),
    service: UserService = Depends(),
):
    return await service.update_company_profile(user_id, data)
