from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base

class UserUseCase(Base):
    __tablename__ = "user_usecase"

    user_usecase_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    usecase_name = Column(String)
    details = Column(String(50))

    stampings = relationship(
        "UserStampingUseCase",
        back_populates="user_usecase",
        cascade="all, delete-orphan"
    )
