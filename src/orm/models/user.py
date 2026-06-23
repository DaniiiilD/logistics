from sqlalchemy import Column, Integer, String, BigInteger
from src.orm.database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    telegram_hash_id = Column(String, unique=True, index=True, nullable=True)
    telegram_id_encrypted=Column(String, nullable=True)

    driver = relationship("Driver", back_populates="user", uselist=False)
    company = relationship("Company", back_populates="user", uselist=False)
