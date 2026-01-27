from sqlalchemy import Column, BigInteger, Date, Integer, String, DateTime, ForeignKey
from .base import Base
from datetime import datetime

class LoyaltyMember(Base):
    __tablename__ = "loyalty_members"

    visitor_id = Column(BigInteger, ForeignKey("visitors.visitor_id"), primary_key=True)
    first_visit = Column(Date)
    last_visit = Column(Date)
    total_visits = Column(Integer)
    loyalty_tier = Column(String(20))   # bronze, silver, gold
    updated_at = Column(DateTime, default=datetime.utcnow)
