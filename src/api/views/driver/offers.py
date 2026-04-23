from fastapi import APIRouter, Depends
from src.api.middlewares.session import in_session
from src.api.middlewares.jwt_token import RoleChecker
from src.core.constants import Role
from api.handlers.driver.offer import DriverOfferService
from src.schemas.responses.offer import OfferResponse

router = APIRouter(prefix="/orders", tags=['Отклики водителя'])

@router.post("/{order_id}/offers", response_model =OfferResponse)
@in_session
async def reply_offer(
    order_id: int,
    user_id: int = Depends(RoleChecker([Role.DRIVER])),
    service: DriverOfferService = Depends()
):
    return await service.create_offer(user_id, order_id)