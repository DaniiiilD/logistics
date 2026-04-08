from pydantic import BaseModel


class VehicleCreate(BaseModel):
    brand: str
    plate_number: str
    model: str
