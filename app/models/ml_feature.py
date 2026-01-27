from sqlalchemy import Column, BigInteger, String, Date, DateTime, ForeignKey, JSON
from datetime import datetime
from .base import Base

class MLFeature(Base):
    __tablename__ = "ml_features"

    feature_id = Column(BigInteger, primary_key=True, index=True)
    video_id = Column(BigInteger, ForeignKey("video_sessions.video_id"))

    feature_date = Column(Date)
    feature_window = Column(String(20))
    features = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
