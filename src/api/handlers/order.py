from fastapi import Depends, HTTPException
from src.orm.repositories.order import OrderRepository
from src.schemas.requests.orders import OrderCreate
from src.orm.models.order import Order
from src.api.services.celery.tasks import send_email_to_driver
from src.orm.repositories.user import UserRepository
from src.orm.repositories.company import CompanyRepository


class OrderService:
    def __init__(
        self,
        order_repo: OrderRepository = Depends(),
        company_repo: CompanyRepository = Depends(),
        user_repo: UserRepository = Depends(),
    ):

        self.order_repo = order_repo
        self.company_repo = company_repo
        self.user_repo = user_repo

    async def create_order(self, data: OrderCreate, user_id: int) -> Order:

        company = await self.company_repo.get_by_user_id(user_id)
        if not company:
            raise HTTPException(status_code=404, detail="Компания не найдена")

        if data.to_date < data.from_date:
            raise HTTPException(
                status_code=400,
                detail="Дата окончания не может быть раньше даты начала",
            )

        order_dict = data.model_dump()
        order_dict["company_id"] = company.id
        new_order = await self.order_repo.create(Order(**order_dict))

        drivers_emails = await self.user_repo.get_email_by_transport(
            new_order.transport_type
        )
        for email in drivers_emails:
            send_email_to_driver.delay(email, new_order.id)

        return new_order
