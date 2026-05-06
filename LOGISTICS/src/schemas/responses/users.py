from pydantic import BaseModel, ConfigDict


class BaseProfileResponse(BaseModel):
    id: int
    email: str
    role: str

    model_config = ConfigDict(from_attributes=True)


class DriverProfileResponse(BaseProfileResponse):
    full_name: str
    phone: str
    transport_type: str

    model_config = ConfigDict(from_attributes=True)


class CompanyProfileResponse(BaseProfileResponse):
    ttn: str
    phone: str
    company_name: str
    rep_full_name: str

    model_config = ConfigDict(from_attributes=True)
