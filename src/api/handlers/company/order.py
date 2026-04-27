from fastapi import Depends, HTTPException
from src.orm.repositories.order import OrderRepository
from src.schemas.requests.orders import OrderCreate, OrderUpdate
from src.orm.models.company.order import Order
from src.api.services.celery.tasks import send_notification_email
from src.orm.repositories.user import UserRepository
from src.orm.repositories.company import CompanyRepository
from src.orm.repositories.driver import DriverRepository
from src.orm.repositories.offer import OfferRepository
from src.api.services.celery.message_text import NotificationMessages
from src.core.constants import OfferStatus, OrderStatus


class OrderService:
    def __init__(
        self,
        order_repo: OrderRepository = Depends(),
        company_repo: CompanyRepository = Depends(),
        user_repo: UserRepository = Depends(),
        driver_repo: DriverRepository = Depends(),
        offer_repo: OfferRepository = Depends(),
    ):

        self.order_repo = order_repo
        self.company_repo = company_repo
        self.user_repo = user_repo
        self.driver_repo = driver_repo
        self.offer_repo = offer_repo

    async def get_company(self, user_id: int):
        """метож чтоб не дублировать код с поиком компании"""
        company = await self.company_repo.get_by_user_id(user_id)
        if not company:
            raise HTTPException(status_code=404, detail="Компания не найдена")
        return company

    async def create_order(self, data: OrderCreate, user_id: int) -> Order:

        company = await self.get_company(user_id)
        order_dict = data.model_dump()
        order_dict["company_id"] = company.id
        new_order = await self.order_repo.create(Order(**order_dict))

        drivers_emails = await self.user_repo.get_email_by_transport(
            new_order.transport_type
        )

        driver_message = NotificationMessages.new_order(
            order_id=new_order.id, transport_type=new_order.transport_type
        )

        for email in drivers_emails:
            send_notification_email.delay(email, new_order.id, driver_message)

        return new_order

    async def get_my_orders(self, user_id) -> list[Order]:
        company = await self.get_company(user_id)
        return await self.order_repo.get_active_order_by_company(company.id)

    async def get_order(self, user_id: int, order_id: int) -> Order:
        order = await self.order_repo.get_order_for_company_by_user(user_id, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Заказ не найден")
        return order

    async def update_order(
        self, user_id: int, order_id: int, data: OrderUpdate
    ) -> Order:
        order = await self.get_order(user_id, order_id)
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="Нет данных для обновления")
        return await self.order_repo.update(order.id, update_data)

    async def delete_order(self, user_id: int, order_id: int):
        order = await self.get_order(user_id, order_id)
        await self.order_repo.update(order.id, {"is_active": False})

    async def accept_offer(self, user_id: int, offer_id: int):
        offer = await self.offer_repo.get_offer_with_relations(offer_id)
        if not offer:
            raise HTTPException(status_code=404, detail="Отклмк не найден")

        order = await self.order_repo.get_order_for_company_by_user(
            user_id, offer.order_id
        )
        if not order:
            raise HTTPException(status_code=403, detail="У вас нет прав на этот заказ")

        await self.offer_repo.update(offer.id, {"status": OfferStatus.ACCEPTED})
        await self.order_repo.update(order.id, {"status": OrderStatus.IN_PROGRESS})

        other_offers = await self.offer_repo.get_other_offers_with_email_for_reject(
            order.id, offer.id
        )

        for other in other_offers:
            await self.offer_repo.update(other.id, {"status": OfferStatus.REJECTED})
            rejected_msg = NotificationMessages.offer_rejected(order_id=order.id)
            send_notification_email.delay(
                other.driver.user.email, order.id, rejected_msg
            )

        accepted_msg = NotificationMessages.offer_accepted(order_id=order.id)
        send_notification_email.delay(offer.driver.user.email, order.id, accepted_msg)

        return {"message": "Исполнитель выбран, остальные заявки отклонены"}

    async def get_order_offers(self, user_id: int, order_id: int):
        order = await self.order_repo.get_order_for_company_by_user(user_id, order_id)
        if not order:
            raise HTTPException(status_code=403, detail="У вас нет прав на этот заказ")

        return await self.offer_repo.get_all_offers_by_order(order.id)
