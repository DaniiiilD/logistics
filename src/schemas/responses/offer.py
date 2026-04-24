from pydantic import BaseModel, ConfigDict


class OfferResponse(BaseModel):
    id: int
    order_id: int
    driver_id: int
    status: str

    model_config = ConfigDict(from_attributes=True)
