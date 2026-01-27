from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime

class Branch(Base):
    __tablename__ = "branches"

    branch_id = Column(BigInteger, primary_key=True, index=True)
    organization_id = Column(BigInteger, ForeignKey("organizations.organization_id"))
    city_id = Column(BigInteger, ForeignKey("cities.city_id"))
    branch_name = Column(String(150))
    address = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

    organization = relationship("Organization")
    city = relationship("City")
