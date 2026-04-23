from sqlalchemy import Column, Integer, String, ForeignKey
from src.orm.database import Base


class Vehicle(Base):
    __tablename__ = "vehicle"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, nullable=False)
    plate_number = Column(String, nullable=False)
    model = Column(String, nullable=False)
    driver_id = Column(
        Integer, ForeignKey("drivers.id", ondelete="CASCADE"), nullable=False
    )
