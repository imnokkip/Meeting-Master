from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from src.models.model import UserCreateModel
from src.database import get_db, reg, auth

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", name="Users", description="регистрация пользователя")
async def register(usr: UserCreateModel, db: Session = Depends(get_db)):
    out = await     reg(usr, db)
    
    if out:
        return {"msg": "ok"}
    
@router.post("/auth", name="Users", description="вход пользователя")
async def authent(resp: Response, usr: UserCreateModel, db: Session = Depends(get_db)):
    out = await auth(resp, usr, db)
    print("yep")
    if out:
        return {"msg": "sucsess"}