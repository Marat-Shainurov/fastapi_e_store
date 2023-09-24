from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from app.database.config import Base, association_table


class Basket(Base):
    __tablename__ = "baskets"

    id = Column(Integer, primary_key=True, index=True)
    products = relationship("Product", secondary=association_table, back_populates="baskets")
