from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey
from .base import Base

class DefectLog(Base):
    __tablename__ = "defect_logs"

    defect_id = Column(BigInteger, primary_key=True, index=True)
    machine_id = Column(BigInteger, ForeignKey("machines.machine_id"))

    defect_type = Column(String(50))
    severity = Column(String(20))
    detected_at = Column(DateTime)
