
from sqlalchemy import Column, BigInteger, String, Time, ForeignKey
from .base import Base

class UserSettings(Base):
    __tablename__ = "user_settings"

    user_id = Column(BigInteger, ForeignKey("users.user_id"), primary_key=True)
    timezone = Column(String(100))
    color_mode = Column(String(20))
    notify_start = Column(Time)
    notify_end = Column(Time)
