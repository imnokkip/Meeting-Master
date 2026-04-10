from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel


DB_URL = "sqlite:///./db/sql_app.db"

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})

class Base(DeclarativeBase): pass

class Rooms(Base):
    __tablename__ = "Rooms"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    places = Column(Integer)

class RoomCreateModel(BaseModel):
    name: str
    places: int

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autoflush=False, bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/rooms', name="Rooms", description="Список комнат", tags=["Rooms"])
async def rooms(db: Session = Depends(get_db)):
    rooms = db.query(Rooms).all()
    s = []
    for i in rooms:
        s.append(i)
    return s

@app.post("/rooms/create")
async def create(room: RoomCreateModel, db: Session = Depends(get_db)):
    # Сначала проверяем вручную (для лучшего UX)
    existing = db.query(Rooms).filter(Rooms.name == room.name).first()
    if existing:
        return {"error": f"Room '{room.name}' already exists"}
    
    try:
        new_room = Rooms(name=room.name, places=room.places)
        db.add(new_room)
        db.commit()
        return {"msg": "ok", "id": new_room.id}
    except IntegrityError:
        db.rollback()
        return {"error": f"Room '{room.name}' already exists"}
    
