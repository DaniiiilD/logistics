from src.orm.models.driver import Driver
from src.orm.repositories.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.orm.database import async_session_factory

class  DriverRepository(BaseRepository):

    model = Driver
        
    async def create(self, user_id: int, full_name: str, 
               phone: str, transport_type: str) ->  Driver:
        async with async_session_factory() as session:
            driver = Driver(
                user_id=user_id,
                full_name = full_name,
                phone = phone,
                transport_type = transport_type    
        )
        session.add(driver)
        await session.commit()
        await session.refresh(driver)
        return driver   