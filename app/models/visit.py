from sqlalchemy import Column, BigInteger, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime

class Visit(Base):
    __tablename__ = "visits"

    visit_id = Column(BigInteger, primary_key=True, index=True)
    visitor_id = Column(BigInteger, ForeignKey("visitors.visitor_id"))
    branch_id = Column(BigInteger, ForeignKey("branches.branch_id"))
    visit_time = Column(DateTime, default=datetime.utcnow)

    visitor = relationship("Visitor")
    branch = relationship("Branch")
