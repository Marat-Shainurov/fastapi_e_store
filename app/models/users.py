from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship, mapped_column

from app.database.config import Base


class User(Base):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    last_name = Column(String, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, index=True, unique=True)
    phone = Column(String, index=True, unique=True)
    hashed_password = Column(String)
    verification_code = Column(String, nullable=True)
    is_active = Column(Boolean, index=True, default=False)
    products = relationship('Product', back_populates='owner')
