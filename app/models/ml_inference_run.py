from sqlalchemy import Column, BigInteger, DateTime, Integer, ForeignKey
from .base import Base

class MLInferenceRun(Base):
    __tablename__ = "ml_inference_runs"

    inference_id = Column(BigInteger, primary_key=True, index=True)
    model_id = Column(BigInteger, ForeignKey("ml_models.model_id"))
    video_id = Column(BigInteger, ForeignKey("video_sessions.video_id"))

    run_time = Column(DateTime)
    processing_time_ms = Column(Integer)
