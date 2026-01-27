from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DateTime, ForeignKey
from datetime import datetime
from .base import Base

class Bus(Base):
    __tablename__ = "buses"

    bus_id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(BigInteger, ForeignKey("organizations.organization_id"))

    bus_number = Column(String(20))
    capacity = Column(Integer)
    driver_name = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
