from sqlalchemy import Column, BigInteger, String, Boolean, DECIMAL
from .base import Base

class MLModel(Base):
    __tablename__ = "ml_models"

    model_id = Column(BigInteger, primary_key=True, index=True)
    model_name = Column(String(100))
    version = Column(String(20))
    accuracy = Column(DECIMAL(5, 2))
    is_active = Column(Boolean, default=True)
