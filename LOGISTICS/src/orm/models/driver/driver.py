from sqlalchemy import Column, Integer, String, ForeignKey
from src.orm.database import Base
from sqlalchemy.orm import relationship


class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    full_name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    transport_type = Column(String, nullable=True)

    user = relationship("User", back_populates="driver")

    order_offers = relationship("OrderOffer", back_populates="driver")
