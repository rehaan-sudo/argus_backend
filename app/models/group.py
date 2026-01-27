from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey
from .base import Base
from datetime import datetime

class Group(Base):
    __tablename__ = "groups"

    group_id = Column(BigInteger, primary_key=True, index=True)
    branch_id = Column(BigInteger, ForeignKey("branches.branch_id"))
    department_name = Column(String(150))
    created_at = Column(DateTime, default=datetime.utcnow)
