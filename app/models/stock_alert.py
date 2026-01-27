from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from .base import Base

class StockAlert(Base):
    __tablename__ = "stock_alerts"

    alert_id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("inventory_items.item_id"))
    alert_type = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
