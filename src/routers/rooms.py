from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import model_room
from database import get_db_room, add, get_all, delete_id

router = APIRouter(prefix="/rooms", tags=["Rooms"])

@router.get('/', name="Rooms", description="Список комнат", tags=["Rooms"])
async def rooms(db: Session = Depends(get_db_room)):
    return get_all(db)

@router.post("/create")
async def create(room: model_room.RoomCreateModel, db: Session = Depends(get_db_room)):
    out = add(room, db)
    if out:
        return {"msg":"ok"}

@router.delete("/delete/{room_id}")
async def delete(room_id: int, db: Session = Depends(get_db_room)):
    dele = delete_id(room_id, db)
    if dele:
        return {"msg": f"ok, id[{room_id}] is delete"}
    else:
        return {"msg": "error"}