from fastapi import Depends, HTTPException
from src.orm.repositories.offer import OfferRepository
from src.orm.repositories.order import OrderRepository
from src.orm.repositories.driver import DriverRepository
from src.orm.models.driver.offer import OrderOffer
from src.core.constants import OrderStatus
from src.api.services.celery.tasks import send_notification_email
from src.api.services.celery.message_text import NotificationMessages


class DriverOfferService:
    def __init__(
        self,
        offer_repo: OfferRepository = Depends(),
        order_repo: OrderRepository = Depends(),
        driver_repo: DriverRepository = Depends(),
    ):

        self.offer_repo = offer_repo
        self.order_repo = order_repo
        self.driver_repo = driver_repo

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

        return saved_offer

    async def get_all_offers(self, user_id: int):
        driver = await self.driver_repo.get_by_user_id(user_id)
        if not driver:
            raise HTTPException(status_code=404, detail="Водитель не найден")

        offers = await self.offer_repo.get_offer_by_driver_id(driver.id)
        return offers

    async def delete_offer(self, user_id: int, offer_id: int):
        driver = await self.driver_repo.get_by_user_id(user_id)
        if not driver:
            raise HTTPException(satatus_code=404, detail="Водитель не найден")

        offer = await self.offer_repo.get_by_id(offer_id)
        if not offer:
            raise HTTPException(status_code=404, detail="Отклик не найден")

        if offer.driver_id != driver.id:
            raise HTTPException(
                status_code=403, detail="Вы не можете удалять чужой отклик"
            )

        await self.offer_repo.delete(offer.id)
