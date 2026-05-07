from pydantic import BaseModel, ConfigDict


class VehicleResponse(BaseModel):
    brand: str
    plate_number: str
    model: str
    id: int

    model_config = ConfigDict(from_attributes=True)
