from src.orm.models.order import Order
from src.orm.repositories.base import BaseRepository
from sqlalchemy import select


class OrderRepository(BaseRepository):
    model = Order

    async def get_active_order_by_company(self, company_id: int):
        query = select(Order).where(
            Order.company_id == company_id,
            Order.is_active
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_active_order_by_id(self, company_id: int, order_id: int):
        query = select(Order).where(
            Order.id == order_id, Order.company_id == company_id,
            Order.is_active 
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
