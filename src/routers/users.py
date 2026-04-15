from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from models import model_user
from database import get_db_user,reg, auth
import tokenizer

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", name="Users", description="регистрация пользователя")
async def register(usr: model_user.UserCreateModel, db: Session = Depends(get_db_user)):
    out = reg(usr, db)
    
    if out:
        return {"msg": "ok"}
    
@router.post("/auth", name="Users", description="вход пользователя")
async def authent(resp: Response, usr: model_user.UserCreateModel, db: Session = Depends(get_db_user)):
    out = auth(resp, usr, db)
    if out:
        return {"msg": "sucsess"}