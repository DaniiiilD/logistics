from sqlalchemy import Column, Integer, String, ForeignKey
from src.orm.database import Base

class Company(Base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    company_name = Column(String, nullable=False)
    ttn = Column(String, nullable=True)
    phone = Column(String, nullable=False)
    rep_full_name = Column(String, nullable=True) 