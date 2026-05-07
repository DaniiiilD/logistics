from src.orm.repositories.base import BaseRepository
from sqlalchemy import select
from src.orm.models.vehicle.vehicle import Vehicle


class VehicleRepository(BaseRepository):
    model = Vehicle

    async def get_vehicle_by_driver_id(self, driver_id: int):
        result = await self.session.execute(
            select(Vehicle).where(Vehicle.driver_id == driver_id)
        )
        return result.scalars().all()
