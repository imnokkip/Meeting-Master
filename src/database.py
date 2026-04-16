from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError
from models.model import Rooms, Users, Base
from time import time
import tokenizer

print(time().__int__())

DB_URL = "sqlite:///./db/sql.db"
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autoflush=False, bind=engine)

# Создаем обе таблицы (Rooms и Users) в одном файле
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_token(session_user: Session, token: str):
    if not token:
        return False
    
    user = session_user.query(Users).filter(Users.token == token).first()
    
    if not user:
        return False
    
    current_time = int(time())
    if user.tk_end and user.tk_end < current_time:
        return False
    
    return True


def get_current_user_from_token(token: str, db_user: Session):
    user = db_user.query(Users).filter(Users.token == token).first()
    
    if not user:
        return None
    
    current_time = int(time())
    if user.tk_end and user.tk_end < current_time:
        return None
    
    return user


def reg(model, session: Session):
    existing = session.query(Users).filter(Users.name == model.name).first()
    if existing:
        return False
    
    try:
        new_usr = Users(name=model.name, password=model.password)
        session.add(new_usr)
        session.commit()
        return True
    except IntegrityError:
        session.rollback()
        return False


def auth(resp, model, session: Session):
    try:
        pers = session.query(Users).filter(Users.name == model.name).first()
        
        if not pers or pers.password != model.password:
            return False
            
        tok = str(tokenizer.generate(pers.name, pers.password))
        
        pers.token = tok
        pers.tk_end = int(time()) + 60
        session.commit()
        
        resp.set_cookie(key="session_token", value=tok, httponly=True)
        return True
    except Exception as e:
        session.rollback()
        return False


def get_all(session: Session):
    vals = session.query(Rooms).all()
    return vals


def add(model, session: Session):
    existing = session.query(Rooms).filter(Rooms.name == model.name).first()
    if existing:
        return False
    
    try:
        new_room = Rooms(name=model.name, places=model.places)
        session.add(new_room)
        session.commit()
        return True
    except IntegrityError:
        session.rollback()
        return False


def delete_id(ids: int, session: Session):
    room = session.query(Rooms).filter(Rooms.id == ids).first()
    if not room:
        return False
    try:
        session.delete(room)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        return False