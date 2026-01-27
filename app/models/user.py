from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True, index=True)
    organization_id = Column(BigInteger, ForeignKey("organizations.organization_id"))
    role_id = Column(BigInteger, ForeignKey("roles.role_id"))

    name = Column(String(100))
    email = Column(String(150), unique=True, index=True)
    phone = Column(String(20))
    password_hash = Column(String(255))

    branch_id = Column(BigInteger, ForeignKey("branches.branch_id"))
    group_id = Column(BigInteger, ForeignKey("groups.group_id"), nullable=True)
    sub_group_id = Column(BigInteger, ForeignKey("sub_groups.sub_group_id"), nullable=True)

    status = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    organization = relationship("Organization")
    role = relationship("Role")
    branch = relationship("Branch")
