from fastapi import APIRouter, Depends
from src.api.middlewares.session import in_session
from src.api.middlewares.jwt_token import RoleChecker
from src.schemas.responses.orders import OrderResponse, OrderWithCostResponse, CostDataResponse
from src.schemas.requests.orders import OrderCreate, OrderUpdate
from src.api.handlers.company.order import OrderService
from src.core.constants import Role
from src.schemas.responses.offer import CompanyViewOfferDriverResponse

router = APIRouter(prefix="/orders", tags=["Заявки компаний"])


@router.post("", response_model=OrderResponse)
@in_session
async def create_order(
    data: OrderCreate,
    user_id: int = Depends(RoleChecker([Role.COMPANY])),
    service: OrderService = Depends(),
):
    return await service.create_order(data, user_id)


@router.get("", response_model=list[OrderWithCostResponse])
@in_session
async def get_my_orders(
    user_id: int = Depends(RoleChecker([Role.COMPANY])),
    service: OrderService = Depends(),
):
    return await service.get_my_orders(user_id)


@router.get("/{order_id}", response_model=OrderWithCostResponse)
@in_session
async def get_order(
    order_id: int,
    user_id: int = Depends(RoleChecker([Role.COMPANY])),
    service: OrderService = Depends(),
):
    return await service.get_order(user_id, order_id)


@router.patch("/{order_id}", response_model=OrderResponse)
@in_session
async def udate_order(
    order_id: int,
    data: OrderUpdate,
    user_id: int = Depends(RoleChecker([Role.COMPANY])),
    service: OrderService = Depends(),
):
    return await service.update_order(user_id, order_id, data)


@router.delete("/{order_id}")
@in_session
async def delete_order(
    order_id: int,
    user_id: int = Depends(RoleChecker([Role.COMPANY])),
    service: OrderService = Depends(),
):
    await service.delete_order(user_id, order_id)
    return {"meassage": "Заказ отменен(скрыт)"}


@router.patch("/offers/{offer_id}/accept")
@in_session
async def accept_driver_offer(
    offer_id: int,
    user_id: int = Depends(RoleChecker([Role.COMPANY])),
    service: OrderService = Depends(),
):
    return await service.accept_offer(user_id, offer_id)


@router.get("/{order_id}/offers", response_model=list[CompanyViewOfferDriverResponse])
@in_session
async def view_order_offers(
    order_id: int,
    user_id: int = Depends(RoleChecker([Role.COMPANY])),
    service: OrderService = Depends(),
):
    return await service.get_order_offers(user_id, order_id)
