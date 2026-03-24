from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class BaseRepository:
    
    model = None
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_by_id(self, id):
        result = await self.session.execute(
            select(self.model).filter(self.model.id == id)
        )
        return result.scalar_one_or_none
    
    async def get_all(self):
        result = await self.session.execute(select(self.model))
        return result.scalars().all()
    
    async def delete(self, id):
        obj =  await self.get_by_id(id)
        if obj:
            await self.session.delete(obj)