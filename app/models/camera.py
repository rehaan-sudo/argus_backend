from sqlalchemy import Column, BigInteger, String, Boolean, Integer, ForeignKey
from .base import Base

class Camera(Base):
    __tablename__ = "cameras"

    camera_id = Column(BigInteger, primary_key=True, index=True)
    machine_id = Column(BigInteger, ForeignKey("machines.machine_id"))
    vpn_confige_id = Column(BigInteger, ForeignKey("vpn_configs.vpn_id"))
    user_name = Column(String(50))
    camera_name = Column(String(50))
    password = Column(String(100))
    camera_type = Column(String(30))   # RTSP, etc.
    ip = Column(String(45))
    cam_zone = Column(String(50))
    is_active = Column(Boolean, default=True)
    port = Column(Integer)
