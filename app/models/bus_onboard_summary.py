from sqlalchemy import Column, Integer, Date, DateTime, ForeignKey
from datetime import datetime
from .base import Base

class BusOnboardSummary(Base):
    __tablename__ = "bus_onboard_summary"

    bus_id = Column(Integer, ForeignKey("buses.bus_id"), primary_key=True)
    date = Column(Date, primary_key=True)

    onboard_students = Column(Integer)
    onboard_teachers = Column(Integer)
    onboard_staff = Column(Integer)
    no_show = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
