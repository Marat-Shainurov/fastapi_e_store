from sqlalchemy import Column, String, Integer, DateTime, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.database.config import Base, association_table


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    price = Column(Float)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_active = Column(Boolean)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="products")

    baskets = relationship("Basket", secondary=association_table, back_populates="products")
