from pydantic import BaseModel, ConfigDict
from datetime import datetime


class OfferResponse(BaseModel):
    id: int
    order_id : int
    driver_id : int
    status: str

    model_config = ConfigDict(from_attributes=True)
