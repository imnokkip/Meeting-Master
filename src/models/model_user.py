from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import DeclarativeBase
from pydantic import BaseModel, Field

class Base(DeclarativeBase): pass

class Users(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    password = Column(String)
    registers = Column(JSON, nullable=True)
    acces_level = Column(Integer, nullable=True)
    token = Column(String, unique=True)
    tk_end = Column(Integer)

class UserCreateModel(BaseModel):
    name: str = Field(..., description="Имя", min_length=4, max_length=50)
    password: str = Field(..., description="Пароль", min_length=4, max_length=50)