from fastapi import APIRouter, Depends
from src.api.middlewares.session import in_session
from src.api.handlers.vehicle import VehicleService
from src.api.middlewares.jwt_token import get_current_user_payload
from src.schemas.requests.vehicles import VehicleCreate
from src.schemas.responses.vehicles import VehicleResponse
from typing import List

vehicle_router = APIRouter(prefix="/vehicles", tags=["Машины"])


@vehicle_router.post("", response_model=VehicleResponse)
@in_session
async def add_vehicle(
    data: VehicleCreate,
    user_id: int = Depends(get_current_user_payload),
    service: VehicleService = Depends(),
):
    return await service.add_vehicle(user_id, data)


@vehicle_router.get("/my", response_model=List[VehicleResponse])
@in_session
async def get_my_vehicles(
    user_id: int = Depends(get_current_user_payload),
    service: VehicleService = Depends(),
):
    return await service.get_my_vehicles(user_id)


@vehicle_router.delete("/{vehicle_id}")
@in_session
async def delete_my_vehicle(
    vehicle_id: int,
    user_id: int = Depends(get_current_user_payload),
    service: VehicleService = Depends(),
):
    await service.delete_vehicle(user_id, vehicle_id)
    return {"message:Машина удалена"}
