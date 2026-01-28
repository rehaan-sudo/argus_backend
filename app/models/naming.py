from sqlalchemy import Column, Integer, String
from .base import Base

class Naming(Base):
    __tablename__ = "naming"

    naming_id = Column(Integer, primary_key=True, index=True)
    naming_tags = Column(String)
