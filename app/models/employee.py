from sqlalchemy import Column, BigInteger, String, Boolean, ForeignKey
from .base import Base

class Employee(Base):
    __tablename__ = "employees"

    employee_id = Column(BigInteger, primary_key=True, index=True)
    branch_id = Column(BigInteger, ForeignKey("branches.branch_id"))
    group_id = Column(BigInteger, ForeignKey("groups.group_id"))
    sub_group_id = Column(BigInteger, ForeignKey("sub_groups.sub_group_id"))

    name = Column(String(100))
    email = Column(String(150))
    phone_num = Column(String(15))
    address = Column(String(255))
    photo_path = Column(String(255))
    is_active = Column(Boolean, default=True)
