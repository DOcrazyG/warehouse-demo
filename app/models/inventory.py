from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from app.core.database import Base
from datetime import datetime


class Inventory(Base):
    __tablename__ = "inventories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text)
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0.0)
    category = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)