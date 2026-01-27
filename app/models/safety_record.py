from sqlalchemy import Column, Integer, String, Date, ForeignKey
from .base import Base

class SafetyRecord(Base):
    __tablename__ = "safety_records"

    safety_id = Column(Integer, primary_key=True, index=True)
    branch_id = Column(Integer, ForeignKey("branches.branch_id"))
    date = Column(Date)
    total_violations = Column(Integer)
    severity_level = Column(String(20))
