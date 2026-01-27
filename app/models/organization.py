from sqlalchemy import Column, BigInteger, String, DateTime
from .base import Base
from datetime import datetime

class Organization(Base):
    __tablename__ = "organizations"

    organization_id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
