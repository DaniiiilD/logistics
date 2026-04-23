from src.orm.repositories.vehicle import VehicleRepository
from src.orm.repositories.driver import DriverRepository
from src.schemas.requests.vehicles import VehicleCreate, VehicleUpdate
from src.schemas.responses.vehicles import VehicleResponse
from fastapi import HTTPException, Depends
from src.orm.models.vehicle import Vehicle
from src.core.constants import MAX_VEHICLES_PER_DRIVER


class VehicleService:
    def __init__(
        self,
        vehicle_repo: VehicleRepository = Depends(),
        driver_repo: DriverRepository = Depends(),
    ):

        self.vehicle_repo = vehicle_repo
        self.driver_repo = driver_repo

    async def add_vehicle(self, user_id: int, data: VehicleCreate) -> VehicleResponse:

        driver = await self.driver_repo.get_by_user_id(user_id)
        if not driver:
            raise HTTPException(status_code=404, detail="Водитель не найден")

        vehicles = await self.vehicle_repo.get_vehicle_by_driver_id(driver.id)

        if len(vehicles) >= MAX_VEHICLES_PER_DRIVER:
            raise HTTPException(
                status_code=400,
                detail=f"Максимум {MAX_VEHICLES_PER_DRIVER} машины",
            )

        vehicle_dict = data.model_dump()
        vehicle_dict["driver_id"] = driver.id

        new_vehicle = await self.vehicle_repo.create(Vehicle(**vehicle_dict))

        return new_vehicle

    async def get_my_vehicles(self, user_id: int) -> list[VehicleResponse]:

        driver = await self.driver_repo.get_by_user_id(user_id)
        if not driver:
            raise HTTPException(status_code=404, detail="Водитель не найден")

        vehicles = await self.vehicle_repo.get_vehicle_by_driver_id(driver.id)

        return vehicles

    async def get_vehicle(self, user_id: int, vehicle_id: int) -> VehicleResponse:
        driver = await self.driver_repo.get_by_user_id(user_id)

        if not driver:
            raise HTTPException(status_code=404, detail="Водитель не найден")

        vehicle = await self.vehicle_repo.get_by_id(vehicle_id)
        if not vehicle:
            raise HTTPException(status_code=404, detail="Трансопрт не найден")

        if vehicle.driver_id != driver.id:
            raise HTTPException(status_code=403, detail="Это не ваша машина")

        return await vehicle

    async def delete_vehicle(self, user_id: int, vehicle_id: int):
        driver = await self.driver_repo.get_by_user_id(user_id)

        if not driver:
            raise HTTPException(status_code=404, detail="Водитель не найден")

        vehicle = await self.vehicle_repo.get_by_id(vehicle_id)
        if not vehicle:
            raise HTTPException(status_code=404, detail="Трансопрт не найден")

        if vehicle.driver_id != driver.id:
            raise HTTPException(status_code=403, detail="Это не ваша машина")

        await self.vehicle_repo.delete(vehicle.id)

    async def update_vehicle(
        self, user_id: int, vehicle_id: int, data: VehicleUpdate
    ) -> VehicleResponse:
        driver = await self.driver_repo.get_by_user_id(user_id)
        if not driver:
            raise HTTPException(status_code=404, detail="Водитель не найден")

        vehicle = self.vehicle_repo.get_by_id(vehicle_id)
        if not vehicle:
            raise HTTPException(status_code=404, detail="Транспорт не найден")

        if vehicle.driver_id != driver.id:
            raise HTTPException(status_code=403, detail="это не ваша машина")

        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="Нет данных для обновления")

        updated_data = await self.vehicle_repo.update(vehicle.id, update_data)
        return updated_data
