from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import DeclarativeBase
from pydantic import BaseModel, Field

class Base(DeclarativeBase): pass

class Rooms(Base):
    __tablename__ = "Rooms"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    places = Column(Integer)

class RoomCreateModel(BaseModel):
    name: str = Field(..., description="Название комнаты", min_length=1, max_length=50)
    places: int = Field(..., description="Количество мест", ge=1, le=1000)