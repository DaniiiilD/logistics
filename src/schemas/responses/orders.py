from pydantic import BaseModel, ConfigDict
from datetime import datetime


class OrderResponse(BaseModel):
    from_date: datetime
    to_date: datetime
    id: int
    company_id: int
    status: str
    transport_type: str

    model_config = ConfigDict(from_attributes=True)
