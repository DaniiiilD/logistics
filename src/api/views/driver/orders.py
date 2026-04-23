from fastapi import APIRouter, Depends
from src.api.middlewares.session import in_session
from src.api.middlewares.jwt_token import RoleChecker
from src.core.constants import Role
from api.handlers.driver.driver import DriverService
from src.schemas.responses.orders import OrderResponse
from typing import Optional
from datetime import datetime

router = APIRouter(prefix="/orders", tags=['Заказы водителя'])

@router.get("", response_model =list[OrderResponse])
@in_session
async def get_suitable_orders(
    from_date: Optional[datetime] = None,
    user_id: int = Depends(RoleChecker([Role.DRIVER])),
    service: DriverService = Depends()
):
    return await service.suitable_orders_for_drivers(user_id, from_date)