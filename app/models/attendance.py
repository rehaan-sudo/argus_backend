from sqlalchemy import Column, BigInteger, Integer, Date, Time, ForeignKey
from .base import Base

class AttendanceLog(Base):
    __tablename__ = "attendance_logs"

    attendance_id = Column(BigInteger, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"))
    date = Column(Date)
    clock_in = Column(Time)
    clock_out = Column(Time)
    status = Column(Integer)  # 1 = present, 0 = absent
