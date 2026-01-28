from sqlalchemy import Column, BigInteger, String, Text, DateTime, ForeignKey
from datetime import datetime
from .base import Base

class Audit(Base):
    __tablename__ = "audits"

    audit_id = Column(BigInteger, primary_key=True, index=True)
    entity_name = Column(String(50))
    entity_id = Column(BigInteger)
    action = Column(String(50))
    actor_user_id = Column(BigInteger, ForeignKey("users.user_id"))
    details = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
