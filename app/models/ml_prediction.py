from sqlalchemy import Column, BigInteger, String, DateTime, DECIMAL, Float, ForeignKey, JSON
from datetime import datetime
from .base import Base

class MLPrediction(Base):
    __tablename__ = "ml_predictions"

    prediction_id = Column(BigInteger, primary_key=True, index=True)
    inference_id = Column(BigInteger, ForeignKey("ml_inference_runs.inference_id"))

    defect_type = Column(String(100))
    confidence = Column(DECIMAL(5, 2))
    bbox = Column(JSON)
    frame_time = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
