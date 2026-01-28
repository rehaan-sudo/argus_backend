from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DateTime, ForeignKey
from datetime import datetime
from .base import Base

class StampingUsecase(Base):
    __tablename__ = "stamping_usecase"

    stamping_usecase_id = Column(Integer, primary_key=True, index=True)
    camera_id = Column(BigInteger, ForeignKey("cameras.camera_id"))
    user_usecase = Column(Integer, ForeignKey("user_usecase.user_feature_id"))

    stamping_usecase = Column(String(100))  # DEFECT_DETECTION, PPE, COUNTING
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
