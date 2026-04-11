from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, Field


DB_ROOM_URL = "sqlite:///./db/sql_rooms.db"
DB_USR_URL = "sqlite:///./db/sql_usrs.db"

room_engine = create_engine(DB_ROOM_URL, connect_args={"check_same_thread": False})
usr_engine = create_engine(DB_USR_URL, connect_args={"check_same_thread": False})

class Base(DeclarativeBase): pass

class Rooms(Base):
    __tablename__ = "Rooms"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    places = Column(Integer)

class RoomCreateModel(BaseModel):
    name: str = Field(..., description="Название комнаты", min_length=1, max_length=50, example="Конференц-зал")
    places: int = Field(..., description="Количество мест", ge=1, le=1000, example=20)

Base.metadata.create_all(bind=room_engine)
Base.metadata.create_all(bind=usr_engine)

Session_room = sessionmaker(autoflush=False, bind=room_engine)
Session_usr = sessionmaker(autoflush=False, bind=usr_engine)

app = FastAPI()

def get_bd_room():
    db = Session_room()
    try:
        yield db
    finally:
        db.close()

@app.get('/rooms', name="Rooms", description="Список комнат", tags=["Rooms"])
async def rooms(db: Session = Depends(get_bd_room)):
    rooms = db.query(Rooms).all()
    s = []
    for i in rooms:
        s.append(i)
    return s

@app.post("/rooms/create")
async def create(room: RoomCreateModel, db: Session = Depends(get_bd_room)):
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
    

@app.delete("/rooms/delete/{room_id}")
def delete(room_id: int, db: Session = Depends(get_bd_room)):
    room = db.query(Rooms).filter(Rooms.id == room_id).first()
    
    if not room:
        return {"error": f"Room with id '{room_id}' not found!"}
    
    try:
        db.delete(room)
        db.commit()
        return {"msg": "ok", "id": room.id}
    except Exception as e:
        db.rollback()
        return {"error": f"Deletion failed: {str(e)}"}