from fastapi import APIRouter, Depends
from src.api.middlewares.session import in_session
from src.api.handlers.vehicle.vehicle import VehicleService
from src.api.middlewares.jwt_token import RoleChecker
from src.schemas.requests.vehicles import VehicleCreate, VehicleUpdate
from src.schemas.responses.vehicles import VehicleResponse
from typing import List
from src.core.constants import Role

router = APIRouter(prefix="/vehicles", tags=["Машины"])


@router.post("", response_model=VehicleResponse)
@in_session
async def add_vehicle(
    data: VehicleCreate,
    user_id: int = Depends(RoleChecker([Role.DRIVER])),
    service: VehicleService = Depends(),
):
    return await service.add_vehicle(user_id, data)


@router.get("", response_model=List[VehicleResponse])
@in_session
async def get_my_vehicles(
    user_id: int = Depends(RoleChecker([Role.DRIVER])),
    service: VehicleService = Depends(),
):
    return await service.get_my_vehicles(user_id)


@router.get("/{vehicle_id}", response_model=VehicleResponse)
@in_session
async def get_vehicle(
    vehicle_id: int,
    user_id: int = Depends(RoleChecker([Role.DRIVER])),
    service: VehicleService = Depends(),
):
    return await service.get_vehicle(user_id, vehicle_id)


@router.delete("/{vehicle_id}")
@in_session
async def delete_my_vehicle(
    vehicle_id: int,
    user_id: int = Depends(RoleChecker([Role.DRIVER])),
    service: VehicleService = Depends(),
):
    await service.delete_vehicle(user_id, vehicle_id)
    return {"message:Машина удалена"}


@router.patch("/{vehicle_id}", response_model=VehicleResponse)
@in_session
async def update_my_vehicle(
    vehicle_id: int,
    data: VehicleUpdate,
    user_id: int = Depends(RoleChecker([Role.DRIVER])),
    service: VehicleService = Depends(),
):
    return await service.update_vehicle(user_id, vehicle_id, data)
