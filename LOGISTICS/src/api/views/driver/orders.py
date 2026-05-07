from fastapi import APIRouter, Depends
from src.api.middlewares.session import in_session
from src.api.middlewares.jwt_token import RoleChecker
from src.core.constants import Role
from src.api.handlers.driver.driver import DriverService
from src.schemas.responses.orders import OrderResponse
from typing import Optional
from datetime import datetime
from src.schemas.responses.offer import OfferResponse
from src.api.handlers.driver.offer import DriverOfferService

router = APIRouter(prefix="/orders", tags=["Заказы водителя"])


@router.get("/suitable", response_model=list[OrderResponse])
@in_session
async def get_suitable_orders(
    from_date: Optional[datetime] = None,
    user_id: int = Depends(RoleChecker([Role.DRIVER])),
    service: DriverService = Depends(),
):
    """Водитель еще не откликнулся, но может отклкнутся на заказы котоые ему подходдят"""
    return await service.suitable_orders_for_drivers(user_id, from_date)


@router.post("/{order_id}/offers", response_model=OfferResponse)
@in_session
async def reply_offer(
    order_id: int,
    user_id: int = Depends(RoleChecker([Role.DRIVER])),
    service: DriverOfferService = Depends(),
):
    return await service.create_offer(user_id, order_id)
