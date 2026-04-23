from fastapi import Depends, HTTPException
from src.orm.repositories.offer import OfferRepository
from src.orm.repositories.order import OrderRepository
from src.orm.repositories.driver import DriverRepository
from src.orm.repositories.company import CompanyRepository
from src.orm.repositories.user import UserRepository
from src.orm.models.driver.offer import OrderOffer
from src.core.constants import OrderStatus 
from src.api.services.celery.tasks import send_notification_email

class DriverOfferService:
    def __init__(
        self,
        offer_repo: OfferRepository = Depends(),
        order_repo: OrderRepository = Depends(),
        driver_repo: DriverRepository = Depends(),
        user_repo: UserRepository = Depends(),
        company_repo: CompanyRepository = Depends()
    ):
        
        self.offer_repo = offer_repo
        self.order_repo = order_repo
        self.driver_repo = driver_repo
        self.user_repo = user_repo
        self.company_repo = company_repo
        
    async def create_offer(self, user_id: int, order_id: int) -> OrderOffer:
        
        driver = await self.driver_repo.get_by_user_id(user_id)
        if not driver:
            raise HTTPException(status_code=404, detail="Водитель не найлен")
        
        order = await self.order_repo.get_by_id(order_id)
        if not order:
            raise HTTPException(status_code=404, detail ="Заказ не найден")
        
        if not order.is_active or order.status != OrderStatus.SEARCH:
            raise HTTPException(status_code=400, detail="Этот заказ не достпуен для отклика")
        
        existing_offer = await self.offer_repo.get_offer(driver.id, order.id)
        if existing_offer:
            raise HTTPException(status_code=400, detail = 'Вы уже откликнулись на этот заказ')
        
        new_offer = OrderOffer(order_id=order.id, driver_id = driver.id)
        saved_offer = await self.offer_repo.create(new_offer)
        
        company = await self.company_repo.get_by_id(order.company_id)
        company_user = await self.user_repo.get_by_id(company.user_id)
        
        message = f"На ваш заказ №{order.id} откликлнулся водитель!"
        send_notification_email.delay(company_user.email, order.id, message)
        
        return saved_offer