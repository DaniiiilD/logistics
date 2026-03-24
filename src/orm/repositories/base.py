from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.orm.database import async_session_factory

class BaseRepository:
    
    model = None
    
    
    async def get_by_id(self, id: int):
        async with async_session_factory() as session:
            result = await session.execute(
                select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none
    
    async def get_all(self):
        async with async_session_factory() as session:
            result = await session.execute(select(self.model))
            return result.scalars().all()
    
    async def delete(self, id: int):
        async with async_session_factory() as session:
            obj =  await self.get_by_id(id)
            if obj:
                await session.delete(obj)
                await session.commit()