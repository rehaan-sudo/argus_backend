from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey
from datetime import datetime
from .base import Base

class AlertLog(Base):
    __tablename__ = "alert_logs"

    alert_log_id = Column(BigInteger, primary_key=True, index=True)
    camera_id = Column(BigInteger, ForeignKey("cameras.camera_id"))
    alert_type = Column(String(100))
    message = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
