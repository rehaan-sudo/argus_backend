from sqlalchemy import Column, BigInteger, Integer, DateTime, ForeignKey
from .base import Base
from datetime import datetime

class ProductionLog(Base):
    __tablename__ = "production_logs"

    production_id = Column(BigInteger, primary_key=True, index=True)
    machine_id = Column(BigInteger, ForeignKey("machines.machine_id"))

    total_material = Column(Integer)
    good_material = Column(Integer)
    defect_material = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
