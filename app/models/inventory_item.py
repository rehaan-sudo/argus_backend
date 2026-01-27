from sqlalchemy import Column, Integer, String
from .base import Base

class InventoryItem(Base):
    __tablename__ = "inventory_items"

    item_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    category = Column(String(50))
    current_quantity = Column(Integer)
    required_quantity = Column(Integer)
    location = Column(String(100))
