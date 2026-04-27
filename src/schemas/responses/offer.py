from pydantic import BaseModel, ConfigDict


class OfferResponse(BaseModel):
    id: int
    order_id: int
    driver_id: int
    status: str

    model_config = ConfigDict(from_attributes=True)


class DriverShortInfo(BaseModel):
    id: int
    full_name: str
    phone: str
    transport_type: str

    model_config = ConfigDict(from_attributes=True)


class CompanyViewOfferDriverResponse(BaseModel):
    id: int
    status: str
    driver: DriverShortInfo

    model_config = ConfigDict(from_attributes=True)
