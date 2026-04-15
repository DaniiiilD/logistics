from src.orm.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(
        Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False
    )
    transport_type = Column(String, nullable=False)
    from_date = Column(DateTime, nullable=False)
    to_date = Column(DateTime, nullable=False)
    status = Column(String, default="search", nullable=False)

    company = relationship("Company", back_populates="orders")
