from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime, timedelta
from .base import Base

class EmailOTP(Base):
    __tablename__ = "email_otp"

    id = Column(Integer, primary_key=True)
    email = Column(String(150), index=True)
    otp_hash = Column(String(255))
    expires_at = Column(DateTime)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
