from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.orm import Session
from src.models.model import RoomCreateModel
from src.database import get_db, add, get_all, delete_id, check_token

ROUTER = APIRouter(prefix="/rooms", tags=["Rooms"])

@ROUTER.get('/', name="Rooms", description="Список комнат", tags=["Rooms"])
async def rooms(db: Session = Depends(get_db)):
    return await get_all(db)

@ROUTER.post("/create")
async def create(
    room: RoomCreateModel, 
    db: Session = Depends(get_db),
    session_token: str = Cookie(None)
):

    if not session_token or not await check_token(db, session_token):
        raise HTTPException(status_code=401, detail="Не авторизован")
    
    out = await add(room, db)
    if out:
        return {"msg": "ok"}
    raise HTTPException(status_code=400, detail="Ошибка создания")

@ROUTER.delete("/delete/{room_id}")
async def delete(
    room_id: int, 
    db: Session = Depends(get_db),
    session_token: str = Cookie(None)
):

    if not session_token or not await check_token(db, session_token):
        raise HTTPException(status_code=401, detail="Не авторизован")
    
    dele = await delete_id(room_id, db)
    if dele:
        return {"msg": f"ok, id[{room_id}] is delete"}
    else:
        raise HTTPException(status_code=404, detail="Комната не найдена")