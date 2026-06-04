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
import uuid
from redis.asyncio import Redis
from src.core.redis import get_redis
from src.core.redis import redis_client
from src.api.services.celery.tasks import send_notification_email
import random
from src.core.security import hash_tg_id, encrypt_tg_id

class UserService:
    def __init__(
        self,
        user_repo: UserRepository = Depends(),
        driver_repo: DriverRepository = Depends(),
        company_repo: CompanyRepository = Depends(),
        redis: Redis = Depends(get_redis),
    ):

        self.user_repo = user_repo
        self.driver_repo = driver_repo
        self.company_repo = company_repo
        self.redis = redis

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

        if update_data.get("email"):
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

    async def create_telegram_link_token(self, user_id: int) -> str:
        """для fast api эндпоинта"""
        token = str(uuid.uuid4())
        key = f"tg_link:{token}"
        await self.redis.setex(key, 600, user_id)
        return token

    async def link_telegram_account(self, token: str, telegram_id: int):
        """для хэндлера тг бота"""
        key = f"tg_link:{token}"
        user_id = await self.redis.get(key)

        if not user_id:
            raise ValueError("Срок действия ссылки истек. Получите новую на сайте.")
        
        update_data = {
            "telegram_hash_id": hash_tg_id(telegram_id),
            "telegram_id_encrypted": encrypt_tg_id(telegram_id),
        }
        
        await self.user_repo.update(int(user_id), update_data)
        await self.redis.delete(key)

    async def get_user_by_tg_id(self, tg_id: int):
        tg_hash = hash_tg_id(tg_id)
        return await self.user_repo.get_user_by_tg_hash(tg_hash)

    async def get_user_by_email(self, email: str):
        return await self.user_repo.get_user_by_email(email)

    async def send_login_code(self, email: str) -> bool:
        code = str(random.randint(100000, 999999))

        key = f"auth_code:{email}"
        await self.redis.setex(key, 300, code)

        send_notification_email.delay(
            email=email, order_id=0, message=f"Ваш код для входа в Telegram-бот:{code}"
        )
        return True

    async def verify_login_user(self, email: str, code: str, telegram_id: int) -> bool:
        key = f"auth_code:{email}"
        saved_code = await self.redis.get(key)

        if saved_code and saved_code == code:
            user = await self.user_repo.get_user_by_email(email)
            if user:
                await self.user_repo.update(user.id, {
                    "telegram_hash_id": hash_tg_id(telegram_id),
                    "telegram_id_encrypted": encrypt_tg_id(telegram_id)
                    })
                return True
        else:
            return False


def create_user_service_manual():
    
    return UserService(
        user_repo=UserRepository(),
        driver_repo=DriverRepository(),
        company_repo=CompanyRepository(),
        redis=redis_client,
    )
    