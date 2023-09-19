from sqlalchemy import Column, Integer, String, Boolean

from app.database.config import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    last_name = Column(String, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, index=True, unique=True)
    phone = Column(String, index=True, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, index=True)
