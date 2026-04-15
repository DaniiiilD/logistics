from fastapi import Depends
from src.orm.repositories.user import UserRepository
from fastapi import HTTPException
from src.schemas.responses.users import (
    DriverProfileResponse,
    CompanyProfileResponse,
)
from src.schemas.requests.users import DriverUpdate, CompanyUpdate
from src.orm.repositories.driver import DriverRepository
from src.orm.repositories.company import CompanyRepository


class UserService:
    def __init__(
        self,
        user_repo: UserRepository = Depends(),
        driver_repo: DriverRepository = Depends(),
        company_repo: CompanyRepository = Depends(),
    ):

        self.user_repo = user_repo
        self.driver_repo = driver_repo
        self.company_repo = company_repo

    async def get_driver_profile(self, user_id: int) -> DriverProfileResponse:
        user = await self.user_repo.get_with_driver(user_id)

        if not user or not user.driver:
            raise HTTPException(status_code=404, detail="Профиль водителя не найден")

        return DriverProfileResponse(
            id=user.id,
            email=user.email,
            role=user.role,
            full_name=user.driver.full_name,
            phone=user.driver.phone,
            transport_type=user.driver.transport_type,
        )

    async def update_driver_profile(
        self, user_id: int, data: DriverUpdate
    ) -> DriverProfileResponse:

        update_data = data.model_dump(exclude_unset=True)

        if not update_data:
            raise HTTPException(status_code=400, detail="Нет данных для обновления")

        user = await self.user_repo.get_by_id(user_id)

        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        if "email" in update_data:
            await self.user_repo.update(user.id, {"email": update_data.pop("email")})

        if update_data:
            driver = await self.driver_repo.get_by_user_id(user_id)
            if driver:
                await self.driver_repo.update(driver.id, update_data)

        return await self.get_driver_profile(user_id)

    async def get_company_profile(self, user_id: int) -> CompanyProfileResponse:
        user = await self.user_repo.get_with_company(user_id)

        if not user or not user.company:
            raise HTTPException(status_code=404, detail="Профиль компании не найден")

        return CompanyProfileResponse(
            id=user.id,
            email=user.email,
            role=user.role,
            ttn=user.company.ttn,
            phone=user.company.phone,
            rep_full_name=user.company.rep_full_name,
            company_name=user.company.company_name,
        )

    async def update_company_profile(
        self, user_id: int, data: CompanyUpdate
    ) -> CompanyProfileResponse:

        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="Нет данных для обновления")

        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        email = update_data.pop("email", None)
        if email:
            await self.user_repo.update(user.id, {"email": email})

        if update_data:
            company = await self.company_repo.get_by_user_id(user_id)
            if company:
                await self.company_repo.update(company.id, update_data)

        return await self.get_company_profile(user_id)
