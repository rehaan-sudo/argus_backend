from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from .base import Base
from datetime import datetime

class CameraLog(Base):
    __tablename__ = "camera_logs"

    id = Column(Integer, primary_key=True, index=True)
    camera_id = Column(Integer, ForeignKey("cameras.camera_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))

    action = Column(String(100))
    details = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
