from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SQLEnum
from src.orm.database import Base
from sqlalchemy.orm import relationship
from src.core.constants import OfferStatus

class OrderOffer(Base):
    __tablename__ = 'order_offers'
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    driver_id = Column(Integer, ForeignKey("drivers.id", ondelete="CASCADE"), nullable=False)
    status = Column(SQLEnum(OfferStatus), default=OfferStatus.PENDING, nullable=False)
    
    order = relationship("Order", back_populates="order_offers")
    driver = relationship("Driver", back_populates="order_offers")
    
    