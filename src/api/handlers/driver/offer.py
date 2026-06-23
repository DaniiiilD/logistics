from fastapi import Depends, HTTPException
from src.orm.repositories.offer import OfferRepository
from src.orm.repositories.order import OrderRepository
from src.orm.repositories.driver import DriverRepository
from src.orm.models.driver.offer import OrderOffer
from src.core.constants import OrderStatus
from src.api.services.celery.tasks import send_notification_email
from src.api.services.celery.message_text import NotificationMessages
from typing import Optional
from src.core.constants import OfferStatus
from src.api.services.centrifugo.realtime import RealtimeService

class DriverOfferService:
    def __init__(
        self,
        offer_repo: OfferRepository = Depends(),
        order_repo: OrderRepository = Depends(),
        driver_repo: DriverRepository = Depends(),
        realtime_service: RealtimeService = Depends(),
    ):

        self.offer_repo = offer_repo
        self.order_repo = order_repo
        self.driver_repo = driver_repo
        self.realtime_service = realtime_service

    async def create_offer(self, user_id: int, order_id: int) -> OrderOffer:

        driver = await self.driver_repo.get_by_user_id(user_id)
        if not driver:
            raise HTTPException(status_code=404, detail="Водитель не найлен")

        order = await self.order_repo.get_order_with_company_user(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Заказ не найден")

        if not order.is_active or order.status != OrderStatus.SEARCH:
            raise HTTPException(
                status_code=400, detail="Этот заказ не достпуен для отклика"
            )

        driver_transport = (driver.transport_type or "").strip().lower()
        order_transport = (order.transport_type or "").strip().lower()
        
        if driver_transport != order_transport:
            raise HTTPException(
                status_code=403,
                detail=f"Тип транспорта водителя {driver.transport_type} не подходит под тип заказа {order.transport_type}"
            )
        
        existing_offer = await self.offer_repo.check_offer_exists(driver.id, order.id)
        if existing_offer:
            raise HTTPException(
                status_code=400, detail="Вы уже откликнулись на этот заказ"
            )

        saved_offer = await self.offer_repo.create(
            OrderOffer(order_id=order.id, driver_id=driver.id)
        )

        message = NotificationMessages.new_offer_to_company(order_id=order.id)

        company_email = order.company.user.email
        send_notification_email.delay(company_email, order.id, message)

        await self.realtime_service.notify_new_offer(
            company_id=order.company_id,
            order_id = order.id,
            driver_name = driver.full_name,
            transport_type=driver.transport_type,
        )
        
        
        return saved_offer

    async def delete_offer(self, user_id: int, offer_id: int):
        driver = await self.driver_repo.get_by_user_id(user_id)
        if not driver:
            raise HTTPException(status_code=404, detail="Водитель не найден")

        offer = await self.offer_repo.get_by_id(offer_id)
        if not offer:
            raise HTTPException(status_code=404, detail="Отклик не найден")

        if offer.driver_id != driver.id:
            raise HTTPException(
                status_code=403, detail="Вы не можете удалять чужой отклик"
            )

        await self.offer_repo.delete(offer.id)

    async def get_my_offers(self, user_id: int, status: Optional[OfferStatus]):
        driver = await self.driver_repo.get_by_user_id(user_id)
        if not driver:
            raise HTTPException(status_code=404, detail="Водитель не найден")

        offers = await self.offer_repo.get_offers_by_driver_id(driver.id, status)
        return offers

    async def get_my_calendar(self, user_id: int):
        driver = await self.driver_repo.get_by_user_id(user_id)
        if not driver:
            raise HTTPException(status_code=404, detail="Водитель не найден")

        accepted_offers = await self.offer_repo.get_accepted_offers_by_driver(driver.id)

        calendar_events = [
            {"from_date": offer.order.from_date, "to_date": offer.order.to_date}
            for offer in accepted_offers
        ]
        return calendar_events


def create_offer_service_manual() -> DriverOfferService:
    
    return DriverOfferService(
        order_repo=OrderRepository(),
        driver_repo=DriverRepository(),
        offer_repo=OfferRepository(),
        realtime_service=RealtimeService(),
    )
