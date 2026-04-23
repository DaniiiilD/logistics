from src.orm.repositories.base import BaseRepository
from src.orm.models.driver.offer import OrderOffer
from sqlalchemy import select

class OfferRepository(BaseRepository):
    model = OrderOffer
    
    async def get_offer(self, driver_id: int, order_id: int):
        """Отклкался ли водитель на этот заказ ранее"""
        query = select(OrderOffer).where(
            OrderOffer.driver_id == driver_id,
            OrderOffer.order_id == order_id
        )
        
        result = await self.session.execute(query)
        return result.scalars_one_or_none()