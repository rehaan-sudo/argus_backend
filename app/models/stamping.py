from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class InfoUseCaseStamping(Base):
    __tablename__ = "info_usecase_stamping"

    stamping_id = Column(Integer, primary_key=True)
    stamping_name = Column(String)
    use_case_id = Column(Integer, ForeignKey("info_use_cases.use_case_id"))

    use_case = relationship("InfoUseCase", back_populates="stampings")
