from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class UserStampingUseCase(Base):
    __tablename__ = "user_stamping_usecase"

    stamping_usecase_id = Column(Integer, primary_key=True)
    user_usecase_id = Column(Integer, ForeignKey("user_usecase.user_usecase_id"))

    user_usecase = relationship(
        "UserUseCase",
        back_populates="stampings"
    )
