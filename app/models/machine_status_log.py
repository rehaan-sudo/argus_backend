from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey, DECIMAL
from .base import Base

class MachineStatusLog(Base):
    __tablename__ = "machine_status_logs"

    status_id = Column(BigInteger, primary_key=True, index=True)
    machine_id = Column(BigInteger, ForeignKey("machines.machine_id"))

    status = Column(String(20))      # RUNNING, STOPPED, IDLE, MAINTENANCE
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    reason = Column(String(100))     # Breakdown, No Material, Power, Setup
    shift = Column(String(10))

    availability = Column(DECIMAL(5, 2))
    performance = Column(DECIMAL(5, 2))
    quality = Column(DECIMAL(5, 2))
    oee_score = Column(DECIMAL(5, 2))
