from sqlalchemy import select
from src.orm.database import db_session


class BaseRepository:
    model = None

    @property
    def session(self):
        return db_session.get()

    async def get_by_id(self, id: int):
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def get_all(self):
        result = await self.session.execute(select(self.model))
        return result.scalars().all()

    async def delete(self, id: int):
        obj = await self.get_by_id(id)
        if obj:
            await self.session.delete(obj)

    async def create(self, obj):
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def update(self, id: int, update_data: dict):
        obj = await self.get_by_id(id)
        if not obj:
            return None

        for key, value in update_data.items():
            setattr(obj, key, value)

        return obj
