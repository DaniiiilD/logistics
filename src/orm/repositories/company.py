from src.orm.models.company import Company
from src.orm.repositories.base import BaseRepository
from sqlalchemy import select


class CompanyRepository(BaseRepository):
    model = Company

    async def get_by_user_id(self, user_id: int):
        result = await self.session.execute(
            select(self.model).where(self.model.user_id == user_id)
        )
        return result.scalar_one_or_none()
