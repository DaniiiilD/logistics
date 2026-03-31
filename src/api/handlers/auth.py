from fastapi import HTTPException, Depends
from src.api.services.utilities.hash_password import get_password_hash
from src.orm.repositories.user import UserRepository
from src.orm.repositories.driver import DriverRepository
from src.orm.repositories.company import CompanyRepository
from src.schemas.requests.auth import DriverCreate, CompanyCreate
from src.schemas.responses.auth import UserResponse
from src.orm.models.user import User
from src.orm.models.company import Company
from src.orm.models.driver import Driver


class RegistrationService:
    def __init__(
        self,
        user_repo: UserRepository = Depends(),
        driver_repo: DriverRepository = Depends(),
        company_repo: CompanyRepository = Depends(),
    ):
        self.user_repo = user_repo
        self.driver_repo = driver_repo
        self.company_repo = company_repo

    async def register_driver(self, driver_data: DriverCreate) -> UserResponse:

        if await self.user_repo.get_by_email(driver_data.email):
            raise HTTPException(status_code=400, detail="Этот email уже занят")

        new_user = User(
            email=driver_data.email,
            hashed_password=get_password_hash(driver_data.password),
            role="driver",
        )
        user = await self.user_repo.create(new_user)

        new_driver = Driver(
            user_id=user.id,
            full_name=driver_data.full_name,
            phone=driver_data.phone,
            transport_type=driver_data.transport_type,
        )

        await self.driver_repo.create(new_driver)

        return UserResponse.model_validate(user)

    async def register_company(self, company_data: CompanyCreate) -> UserResponse:

        if await self.user_repo.get_by_email(company_data.email):
            raise HTTPException(status_code=400, detail="Этот email уже занят")

        new_user = User(
            email=company_data.email,
            hashed_password=get_password_hash(company_data.password),
            role="company",
        )
        user = await self.user_repo.create(new_user)

        new_company = Company(
            user_id=user.id,
            company_name=company_data.company_name,
            ttn=company_data.ttn,
            phone=company_data.phone,
            rep_full_name=company_data.rep_full_name,
        )
        await self.company_repo.create(new_company)

        return UserResponse.model_validate(user)
