from sqlalchemy import Column, Integer, String, Boolean

from app.database.config import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, index=True)
    phone = Column(String, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, index=True)
