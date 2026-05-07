from pydantic import BaseModel, ConfigDict
from datetime import datetime


class OrderResponse(BaseModel):
    from_date: datetime
    to_date: datetime
    id: int
    company_id: int
    status: str
    transport_type: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class CostDataResponse(BaseModel):
    price_per_day: int
    total_price: int
    
class OrderWithCostResponse(BaseModel):
    order: OrderResponse
    accounting: CostDataResponse | None