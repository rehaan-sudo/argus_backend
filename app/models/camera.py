from sqlalchemy import Column, BigInteger, String, Boolean, Integer, ForeignKey
from .base import Base

class Camera(Base):
    __tablename__ = "cameras"

    camera_id = Column(BigInteger, primary_key=True, index=True)
    machine_id = Column(BigInteger, ForeignKey("machines.machine_id"))
    vpn_confige = Column(BigInteger, ForeignKey("vpn_configs.vpn_id"))

    camera_name = Column(String(50))
    camera_type = Column(String(30))   # RTSP, etc.
    IP = Column(String(50))
    cam_zone = Column(String(50))
    is_active = Column(Boolean, default=True)
    port = Column(Integer)
