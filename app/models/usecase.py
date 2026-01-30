from sqlalchemy import Column, Integer, String, Boolean, Text
from sqlalchemy.orm import relationship
from .base import Base

class InfoUseCase(Base):
    __tablename__ = "info_use_cases"

    use_case_id = Column(Integer, primary_key=True)
    use_case_name = Column(String)
    description = Column(Text)
    is_active = Column(Boolean, default=True)

    stampings = relationship("InfoUseCaseStamping", back_populates="use_case")
