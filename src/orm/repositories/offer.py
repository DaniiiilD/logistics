from src.orm.repositories.base import BaseRepository
from src.orm.models.driver.offer import OrderOffer
from sqlalchemy import select


class OfferRepository(BaseRepository):
    model = OrderOffer

    async def check_offer_exists(self, driver_id: int, order_id: int):
        """Отклкался ли водитель на этот заказ ранее"""
        query = select(OrderOffer).where(
            OrderOffer.driver_id == driver_id, OrderOffer.order_id == order_id
        )

        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_offer_by_driver_id(self, driver_id):
        result = await self.session.execute(
            select(OrderOffer).where(OrderOffer.driver_id == driver_id)
        )
        return result.scalars().all()
