from pydantic import BaseModel
from typing import Optional


class VehicleCreate(BaseModel):
    brand: str
    plate_number: str
    model: str


class VehicleUpdate(BaseModel):
    brand: Optional[str] = None
    plate_number: Optional[str] = None
    model: Optional[str] = None
