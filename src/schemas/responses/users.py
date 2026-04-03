from pydantic import BaseModel, ConfigDict
from typing import Union


class BaseProfileResponse(BaseModel):
    id: int
    email: str
    role: str


model_config = ConfigDict(from_attributes=True)


class DriverProfileResponse(BaseProfileResponse):
    full_name: str
    phone: str
    transport_type: str


class CompanyProfileResponse(BaseProfileResponse):
    ttn: str
    phone: str
    company_name: str
    rep_full_name: str


ProfileResponse = Union[DriverProfileResponse, CompanyProfileResponse]
