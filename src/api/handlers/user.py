from fastapi import Depends
from src.orm.repositories.user import UserRepository
from fastapi import HTTPException
from src.schemas.responses.users import (
    ProfileResponse,
    DriverProfileResponse,
    CompanyProfileResponse,
)
from src.schemas.requests.users import ProfileUpdate
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

    async def get_profile(self, user_id: int) -> ProfileResponse:
        user = await self.user_repo.get_by_id(user_id)

        if not user:
            raise HTTPException(status_code=401, detail="пользователь не найден")

        if user.role == "driver":
            driver = await self.driver_repo.get_by_user_id(user_id)

            if not driver:
                raise HTTPException(
                    status_code=404, detail="Профиль водителя не найден"
                )

            return DriverProfileResponse(
                id=user.id,
                email=user.email,
                role=user.role,
                full_name=driver.full_name,
                phone=driver.phone,
                transport_type=driver.transport_type,
            )

        elif user.role == "company":
            company = await self.company_repo.get_by_user_id(user_id)

            if not company:
                raise HTTPException(
                    status_code=404, detail="Профиль компании не найден"
                )

            return CompanyProfileResponse(
                id=user.id,
                email=user.email,
                role=user.role,
                ttn=company.ttn,
                phone=company.phone,
                rep_full_name=company.rep_full_name,
                company_name=company.company_name,
            )

    async def update_profile(
        self, user_id: int, data: ProfileUpdate
    ) -> ProfileResponse:

        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="Нет данных для обновления")

        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        user_updates = {}
        if "email" in update_data:
            user_updates["email"] = update_data.pop("email")

        if user_updates:
            await self.user_repo.update(user.id, user_updates)

        if update_data:
            if user.role == "driver":
                driver = await self.driver_repo.get_by_user_id(user_id)
                if driver:
                    await self.driver_repo.update(driver.id, update_data)

            elif user.role == "company":
                company = await self.company_repo.get_by_user_id(user_id)
                if company:
                    await self.company_repo.update(company.id, update_data)

        return await self.get_profile(user_id)
