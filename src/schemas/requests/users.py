from pydantic import BaseModel, EmailStr
from typing import Optional


class DriverUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    transport_type: Optional[str] = None


class CompanyUpdate(BaseModel):
    email: Optional[EmailStr] = None
    company_name: Optional[str] = None
    ttn: Optional[str] = None
    phone: Optional[str] = None
    rep_full_name: Optional[str] = None
