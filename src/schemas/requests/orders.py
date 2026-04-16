from pydantic import BaseModel, model_validator
from datetime import datetime
from typing import Optional


class OrderCreate(BaseModel):
    from_date: datetime
    to_date: datetime
    transport_type: str

    @model_validator(mode="after")
    def check_dates(self):
        if self.to_date < self.from_date:
            raise ValueError("Дата окончания не может быть раньше даты начала")
        return self


class OrderUpdate(BaseModel):
    transport_type: Optional[str] = None
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None
    status: Optional[str] = None

    @model_validator(mode="after")
    def check_dates(self):
        if self.from_date and self.to_date and self.to_date < self.from_date:
            raise ValueError("Дата окончания не может быть раньше даты начала")
        return self
