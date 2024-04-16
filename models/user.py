from sqlalchemy import Column, String
from models.base_model import BaseModel, Base

class User(BaseModel, Base):
    """User class"""
    __tablename__ = "users"
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128))
    last_name = Column(String(128)
