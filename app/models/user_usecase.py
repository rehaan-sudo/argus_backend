from sqlalchemy import Column, Integer, String, ForeignKey
from .base import Base

class UserUseCase(Base):
    __tablename__ = "user_usecase"

    user_feature_id = Column(Integer, primary_key=True, index=True)
    branch_id = Column(Integer, ForeignKey("branches.branch_id"))
    usecase = Column(String)
    details = Column(String(50))
