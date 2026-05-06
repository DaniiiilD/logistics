from pydantic import BaseModel


class DriverCreate(BaseModel):
    email: str
    password: str
    full_name: str
    phone: str
    transport_type: str


class CompanyCreate(BaseModel):
    email: str
    password: str
    company_name: str
    ttn: str
    phone: str
    rep_full_name: str
