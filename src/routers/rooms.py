from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.orm import Session
from models.model import RoomCreateModel
from database import get_db, add, get_all, delete_id, check_token

router = APIRouter(prefix="/rooms", tags=["Rooms"])

@router.get('/', name="Rooms", description="Список комнат", tags=["Rooms"])
async def rooms(db: Session = Depends(get_db)):
    return get_all(db)

@router.post("/create")
async def create(
    room: RoomCreateModel, 
    db: Session = Depends(get_db),
    session_token: str = Cookie(None)
):

    if not session_token or not check_token(db, session_token):
        raise HTTPException(status_code=401, detail="Не авторизован")
    
    out = add(room, db)
    if out:
        return {"msg": "ok"}
    raise HTTPException(status_code=400, detail="Ошибка создания")

@router.delete("/delete/{room_id}")
async def delete(
    room_id: int, 
    db: Session = Depends(get_db),
    session_token: str = Cookie(None)
):

    if not session_token or not check_token(db, session_token):
        raise HTTPException(status_code=401, detail="Не авторизован")
    
    dele = delete_id(room_id, db)
    if dele:
        return {"msg": f"ok, id[{room_id}] is delete"}
    else:
        raise HTTPException(status_code=404, detail="Комната не найдена")