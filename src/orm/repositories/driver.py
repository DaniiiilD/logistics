from src.orm.models.driver import Driver
from sqlalchemy import select
from src.orm.repositories.base import BaseRepository


class DriverRepository(BaseRepository):
    model = Driver

    async def get_by_user_id(self, user_id: int) -> Driver | None:
        result = await self.session.execute(
            select(Driver).where(Driver.user_id == user_id)
        )
        return result.scalar_one_or_none()
