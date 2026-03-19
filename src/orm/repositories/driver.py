from sqlalchemy.orm import Session
from src.orm.models.driver import Driver
from src.orm.repositories.base import BaseRepository


class  DriverRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(Driver, db)
        
    def create(self, user_id: int, full_name: str, 
               phone: str, transport_type: str) ->  Driver:
        driver = Driver(
            user_id=user_id,
            full_name = full_name,
            phone = phone,
            transport_type = transport_type    
        )
        self.db.add(driver)
        return driver   