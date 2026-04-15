from pydantic import BaseModel
from datetime import datetime


class OrderCreate(BaseModel):
    from_date: datetime
    to_date: datetime
    transport_type: str
