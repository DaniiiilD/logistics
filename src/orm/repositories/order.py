from datetime import datetime
from typing import Optional
from src.orm.models.order import Order
from src.orm.models.company import Company
from src.orm.repositories.base import BaseRepository
from sqlalchemy import select
from src.core.constants import OrderStatus

class OrderRepository(BaseRepository):
    model = Order
    
    async def get_suitable_orders(
        self, 
        transport_type : str,
        status: OrderStatus,
        min_date: Optional[datetime] = None
    ):
        query = select(Order).where(
            Order.transport_type == transport_type,
            Order.status == status,
            Order.is_active == True
        )
        
        if min_date:
            query = query.where(Order.from_date >= min_date)
            
        result = await self.session.execute(query)
        return result.scalars().all()

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
    
    
    async def get_order_for_company_by_user(self, user_id: int, order_id: int):
        query = (
            select(Order)
            .join(Company, Order.company_id == Company.id)
            .where(
                Company.user_id == user_id,
                Order.id == order_id,
                Order.is_active == True
            )
        )
        
        result = await self.session.execute(query)
        return result.scalar_one_or_none()