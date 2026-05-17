from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=True) # Adding email field
    hashed_password = Column(String, nullable=False)
    role = Column(String(50), server_default="user", nullable=False)