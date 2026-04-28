from src.orm.repositories.base import BaseRepository
from src.orm.models.driver.offer import OrderOffer
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.core.constants import OfferStatus
from src.orm.models.driver.driver import Driver
from typing import Optional


class OfferRepository(BaseRepository):
    model = OrderOffer

    async def check_offer_exists(self, driver_id: int, order_id: int):
        """Отклкался ли водитель на этот заказ ранее"""
        query = select(OrderOffer).where(
            OrderOffer.driver_id == driver_id, OrderOffer.order_id == order_id
        )

        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_offers_by_driver_id(self, driver_id: int):
        result = await self.session.execute(
            select(OrderOffer).where(OrderOffer.driver_id == driver_id)
        )
        return result.scalars().all()

    async def get_all_offers_by_order(self, order_id: int):
        query = (
            select(OrderOffer)
            .options(selectinload(OrderOffer.driver))
            .where(OrderOffer.order_id == order_id)
        )

        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_other_offers_with_email_for_reject(
        self, order_id: int, winner_offer_id: int
    ):
        query = (
            select(OrderOffer)
            .options(selectinload(OrderOffer.driver).selectinload(Driver.user))
            .where(
                OrderOffer.order_id == order_id,
                OrderOffer.id != winner_offer_id,
                OrderOffer.status == OfferStatus.PENDING,
            )
        )

        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_offer_with_relations(self, offer_id: int):
        query = (
            select(OrderOffer)
            .options(selectinload(OrderOffer.driver).selectinload(Driver.user))
            .where(OrderOffer.id == offer_id)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_offers_by_driver_id(self, driver_id: int, status: Optional[OfferStatus] = None):
        query = (
            select(OrderOffer)
            .options(selectinload(OrderOffer.order))
            .where(OrderOffer.driver_id == driver_id)
        )
        
        if status:
            query = query.where(OrderOffer.status == status)
        
        result = await self.session.execute(query)
        return result.scalars().all()
            
    async def get_accepted_offers_by_driver(self, driver_id: int):
        query = (
            select(OrderOffer)
            .options(selectinload(OrderOffer.order))
            .where(OrderOffer.driver_id == driver_id,
                   OrderOffer.status == OfferStatus.ACCEPTED
            )
        )
        
        result = await self.session.execute(query)
        return result.scalars().all()
        