from sqlalchemy import Column, BigInteger, DateTime, ForeignKey
from .base import Base

class VideoSession(Base):
    __tablename__ = "video_sessions"

    video_id = Column(BigInteger, primary_key=True, index=True)
    camera_id = Column(BigInteger, ForeignKey("cameras.camera_id"))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
