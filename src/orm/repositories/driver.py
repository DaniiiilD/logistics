from src.orm.models.driver import Driver
from src.orm.repositories.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class  DriverRepository(BaseRepository):

    model = Driver
        
    async def create(self, user_id: int, full_name: str, 
               phone: str, transport_type: str) ->  Driver:
        driver = Driver(
            user_id=user_id,
            full_name = full_name,
            phone = phone,
            transport_type = transport_type    
        )
        self.session.add(driver)
        return driver   