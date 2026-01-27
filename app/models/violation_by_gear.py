from sqlalchemy import Column, Integer, String, ForeignKey
from .base import Base

class ViolationByGear(Base):
    __tablename__ = "violation_by_gear"

    id = Column(Integer, primary_key=True, index=True)
    safety_id = Column(Integer, ForeignKey("safety_records.safety_id"))
    gear_type = Column(String(50))
    count = Column(Integer)
