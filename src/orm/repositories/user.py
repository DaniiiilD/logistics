from src.orm.models.user import User
from src.orm.models.driver.driver import Driver
from src.orm.repositories.base import BaseRepository
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy import func


class UserRepository(BaseRepository):
    model = User

    async def get_user_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(User)
            .where(func.lower(User.email) == email.lower().strip())
            .options(selectinload(User.driver))
        )
        return result.scalar_one_or_none()

    async def get_with_driver(self, user_id: int) -> User | None:
        query = (
            select(User).options(selectinload(User.driver)).where(User.id == user_id)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_with_company(self, user_id: int) -> User | None:
        query = (
            select(User).options(selectinload(User.company)).where(User.id == user_id)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_email_by_transport(self, transport_type: str) -> list[str]:
        """Ищем email вскх водитеой с подходящим типом транспорта"""
        query = (
            select(User.email)
            .join(User.driver)
            .where(func.lower(Driver.transport_type) == transport_type.lower().strip())
        )

        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_user_by_tg_id(self, tg_id: int):
        result = await self.session.execute(
            select(User)
            .where(User.telegram_id == tg_id)
            .options(selectinload(User.driver))
        )
        return result.scalar_one_or_none()

    async def get_driver_tg_ids_by_transport_type(
        self, transport_type: str
    ) -> list[int]:
        query = (
            select(User.telegram_id)
            .join(Driver)
            .where(
                func.lower(Driver.transport_type) == transport_type.lower().strip(),
                User.telegram_id.is_not(None),
            )
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())
