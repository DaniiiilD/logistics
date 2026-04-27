from fastapi import Depends, HTTPException
from src.orm.repositories.order import OrderRepository
from src.orm.models.company.order import Order
from src.orm.repositories.driver import DriverRepository
from datetime import datetime
from typing import Optional
from src.core.constants import OrderStatus


class DriverService:
    def __init__(
        self,
        order_repo: OrderRepository = Depends(),
        driver_repo: DriverRepository = Depends(),
    ):

        self.order_repo = order_repo
        self.driver_repo = driver_repo

    async def suitable_orders_for_drivers(
        self, user_id: int, from_date: Optional[datetime]
    ) -> list[Order]:
        driver = await self.driver_repo.get_by_user_id(user_id)
        if not driver:
            raise HTTPException(status_code=404, detail="Водиетль не найден")
        driver_transport = driver.transport_type
        if driver_transport is None:
            return []

        return await self.order_repo.get_suitable_orders(
            transport_type=driver.transport_type,
            status=OrderStatus.SEARCH,
            min_date=from_date,
        )
