from src.orm.models.user import User
from src.orm.models.driver import Driver
from src.orm.repositories.base import BaseRepository
from sqlalchemy import select
from sqlalchemy.orm import selectinload


class UserRepository(BaseRepository):
    model = User

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(select(User).where(User.email == email))
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
            .where(Driver.transport_type == transport_type)
        )

        result = await self.session.execute(query)
        return list(result.scalars().all())
