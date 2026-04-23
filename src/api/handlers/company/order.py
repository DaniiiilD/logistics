from fastapi import Depends, HTTPException
from src.orm.repositories.order import OrderRepository
from src.schemas.requests.orders import OrderCreate, OrderUpdate
from src.orm.models.company.order import Order
from src.api.services.celery.tasks import send_notification_email
from src.orm.repositories.user import UserRepository
from src.orm.repositories.company import CompanyRepository
from src.orm.repositories.driver import DriverRepository


class OrderService:
    def __init__(
        self,
        order_repo: OrderRepository = Depends(),
        company_repo: CompanyRepository = Depends(),
        user_repo: UserRepository = Depends(),
        driver_repo: DriverRepository = Depends()
    ):

        self.order_repo = order_repo
        self.company_repo = company_repo
        self.user_repo = user_repo
        self.driver_repo = driver_repo

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
        
        driver_message = (
            f'Здравствуйте, Появилась новая заявка на перевозку {new_order.id}.'
            f'Требуемый транспорт: {new_order.transport_type}.'
            f'Зайдите в прилодение, чтобы откликнутся.'
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
        