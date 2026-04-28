from fastapi import APIRouter, Depends
from src.api.middlewares.session import in_session
from src.api.middlewares.jwt_token import RoleChecker
from src.core.constants import Role
from typing import List, Optional
from api.handlers.driver.offer import DriverOfferService
from src.schemas.responses.offer import OfferResponse, DriverViewOfferResponse, DriverCalendarEvent
from src.core.constants import OfferStatus


router = APIRouter(prefix="/offers", tags=["Отклики водителя"])


@router.get("", response_model=List[OfferResponse])
@in_session
async def get_all_offers(
    user_id: int = Depends(RoleChecker([Role.DRIVER])),
    service: DriverOfferService = Depends(),
):
    return await service.get_all_offers(user_id)


@router.delete("/{offer_id}")
@in_session
async def delete_my_offer(
    offer_id: int,
    user_id: int = Depends(RoleChecker([Role.DRIVER])),
    service: DriverOfferService = Depends(),
):
    await service.delete_offer(user_id, offer_id)
    return {"message": "Отлик успешно отозван"}

@router.get('', response_model = List[DriverViewOfferResponse])
@in_session
async def get_my_offers(
    status: Optional[OfferStatus] = None,
    user_id: int = Depends(RoleChecker([Role.DRIVER])),
    service: DriverOfferService = Depends()
):
    return await service.get_my_offers(user_id, status)
    

@router.get('/calendar', response_model = List[DriverCalendarEvent])
@in_session
async def get_mt_calendar(
    user_id: int = Depends(RoleChecker([Role.DRIVER])),
    service: DriverOfferService = Depends()
):
    return await service.get_my_calendar(user_id)