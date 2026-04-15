from fastapi import APIRouter, Depends
from src.api.middlewares.session import in_session
from src.api.middlewares.jwt_token import RoleChecker
from src.schemas.responses.orders import OrderResponse
from src.schemas.requests.orders import OrderCreate
from src.api.handlers.order import OrderService

order_router = APIRouter(prefix="/orders", tags=["Заявки компаний"])


@order_router.post("", response_model=OrderResponse)
@in_session
async def create_order(
    data: OrderCreate,
    user_id: int = Depends(RoleChecker(["company"])),
    service: OrderService = Depends(),
):
    return await service.create_order(data, user_id)
