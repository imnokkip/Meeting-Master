from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import bd_rooms
import models
import uvicorn

app = FastAPI()

@app.get('/rooms', name="Rooms", description="Список комнат", tags=["Rooms"])
async def rooms(db: Session = Depends(bd_rooms.Rooms_bd.get_bd_room)):
    rooms = db.query(models.Rooms).all()
    s = []
    for i in rooms:
        s.append(i)
    return s

@app.post("/rooms/create")
async def create(room: models.RoomCreateModel, db: Session = Depends(bd_rooms.Rooms_bd.get_bd_room)):
    # Сначала проверяем вручную (для лучшего UX)
    existing = db.query(models.Rooms).filter(models.Rooms.name == room.name).first()
    if existing:
        return {"error": f"Room '{room.name}' already exists"}
    
    try:
        new_room = models.Rooms(name=room.name, places=room.places)
        db.add(new_room)
        db.commit()
        return {"msg": "ok", "id": new_room.id}
    except IntegrityError:
        db.rollback()
        return {"error": f"Room '{room.name}' already exists"}
    

@app.delete("/rooms/delete/{room_id}")
def delete(room_id: int, db: Session = Depends(bd_rooms.Rooms_bd.get_bd_room)):
    room = db.query(models.Rooms).filter(models.Rooms.id == room_id).first()
    
    if not room:
        return {"error": f"Room with id '{room_id}' not found!"}
    
    
    try:
        db.delete(room)
        db.commit()
        return {"msg": "ok", "id": room.id}
    except Exception as e:
        db.rollback()
        return {"error": f"Deletion failed: {str(e)}"}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("routers:app", host="127.0.0.1", port=8000, reload=True)