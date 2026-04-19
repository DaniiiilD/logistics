from fastapi import APIRouter, Depends
from src.api.middlewares.session import in_session
from src.api.middlewares.jwt_token import RoleChecker
from src.core.constants import Role
from src.api.handlers.order import OrderService
from src.schemas.responses.orders import OrderResponse

router = APIRouter(prefix="/orders", tags=['Заказы водителя'])

@router.get("", response_model =list[OrderResponse])
@in_session
async def get_suitable_orders(
    user_id: int = Depends(RoleChecker([Role.DRIVER])),
    service: OrderService = Depends()
):
    return await service.suitable_orders_for_drivers(user_id)