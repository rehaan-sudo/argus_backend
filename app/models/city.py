from sqlalchemy import Column, Integer, String
from .base import Base

class City(Base):
    __tablename__ = "cities"

    city_id = Column(Integer, primary_key=True, index=True)
    city_name = Column(String(100))
    state = Column(String(100))
    country = Column(String(100))
