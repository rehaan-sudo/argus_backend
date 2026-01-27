from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey
from .base import Base

class PPEViolation(Base):
    __tablename__ = "ppe_violations"

    violation_id = Column(BigInteger, primary_key=True, index=True)
    camera_id = Column(BigInteger, ForeignKey("cameras.camera_id"))

    ppe_type = Column(String(50))
    person_type = Column(String(20))
    detected_at = Column(DateTime)
