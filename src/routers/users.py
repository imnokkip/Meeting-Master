from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import model_user
from database import get_db_user,reg

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", name="Users", description="регистрация пользователя")
async def register(usr: model_user.UserCreateModel, db: Session = Depends(get_db_user)):
    out = reg(usr, db)
    if out:
        return {"msg": "ok"}