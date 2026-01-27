from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, ForeignKey
from .base import Base
from datetime import datetime

class VPNConfig(Base):
    __tablename__ = "vpn_configs"

    vpn_id = Column(BigInteger, primary_key=True, index=True)
    branch_id = Column(BigInteger, ForeignKey("branches.branch_id"))

    username = Column(String(100))
    password = Column(String(20))
    site = Column(String(10))
    config_file_path = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
