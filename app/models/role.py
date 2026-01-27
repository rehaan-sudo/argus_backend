from sqlalchemy import Column, BigInteger, String
from .base import Base

class Role(Base):
    __tablename__ = "roles"

    role_id = Column(BigInteger, primary_key=True, index=True)
    role_name = Column(String(50), unique=True, nullable=False)
