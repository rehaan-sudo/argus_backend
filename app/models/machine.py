from sqlalchemy import Column, BigInteger, String, Boolean, ForeignKey
from .base import Base

class Machine(Base):
    __tablename__ = "machines"

    machine_id = Column(BigInteger, primary_key=True, index=True)
    subgroup_id = Column(BigInteger, ForeignKey("sub_groups.sub_group_id"))
    machine_code = Column(String(50))
    location = Column(String(100))
    is_active = Column(Boolean, default=True)
