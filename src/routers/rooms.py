from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.orm import Session
from models import model_room
from database import get_db_room, add, get_all, delete_id, get_db_user, check_token

router = APIRouter(prefix="/rooms", tags=["Rooms"])

@router.get('/', name="Rooms", description="Список комнат", tags=["Rooms"])
async def rooms(db_room: Session = Depends(get_db_room)):
    # Для списка комнат проверка не обязательна (можно оставить открытым)
    return get_all(db_room)

@router.post("/create")
async def create(
    room: model_room.RoomCreateModel, 
    db_room: Session = Depends(get_db_room),
    db_user: Session = Depends(get_db_user),  # Добавляем БД пользователей
    session_token: str = Cookie(None)  # Получаем токен из куки
):
    # Проверяем авторизацию
    if not session_token or not check_token(db_user, session_token):
        raise HTTPException(status_code=401, detail="Не авторизован")
    
    out = add(room, db_room)
    if out:
        return {"msg": "ok"}
    raise HTTPException(status_code=400, detail="Ошибка создания")

@router.delete("/delete/{room_id}")
async def delete(
    room_id: int, 
    db_room: Session = Depends(get_db_room),
    db_user: Session = Depends(get_db_user),  # Добавляем БД пользователей
    session_token: str = Cookie(None)  # Получаем токен из куки
):
    # Проверяем авторизацию
    if not session_token or not check_token(db_user, session_token):
        raise HTTPException(status_code=401, detail="Не авторизован")
    
    dele = delete_id(room_id, db_room)
    if dele:
        return {"msg": f"ok, id[{room_id}] is delete"}
    else:
        raise HTTPException(status_code=404, detail="Комната не найдена")