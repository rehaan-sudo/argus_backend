from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey
from .base import Base
from datetime import datetime

class SubGroup(Base):
    __tablename__ = "sub_groups"

    sub_group_id = Column(BigInteger, primary_key=True, index=True)
    group_id = Column(BigInteger, ForeignKey("groups.group_id"))
    sub_group_name = Column(String(150))
    created_at = Column(DateTime, default=datetime.utcnow)
