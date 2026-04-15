from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError
from models import model_room, model_user
from time import time
import tokenizer

print(time().__int__())

DB_ROOM_URL = "sqlite:///./db/sql_rooms.db"
room_engine = create_engine(DB_ROOM_URL, connect_args={"check_same_thread": False})
SessionRoom = sessionmaker(autoflush=False, bind=room_engine)
model_room.Base.metadata.create_all(bind=room_engine)


DB_USER_URL = "sqlite:///./db/sql_users.db"
user_engine = create_engine(DB_USER_URL, connect_args={"check_same_thread": False})
SessionUser = sessionmaker(autoflush=False, bind=user_engine)
model_user.Base.metadata.create_all(bind=user_engine)

def get_db_room():
    db = SessionRoom()
    try:
        yield db
    finally:
        db.close()

def get_db_user():
    db = SessionUser()
    try:
        yield db
    finally:
        db.close()


def check_token(session_user, token):
    if not token:
        return False
    
    user = session_user.query(model_user.Users).filter(
        model_user.Users.token == token
    ).first()
    
    if not user:
        return False
    
    current_time = int(time())
    if user.tk_end and user.tk_end < current_time:
        return False
    
    return True

def get_current_user_from_token(token: str, db_user: Session):
    user = db_user.query(model_user.Users).filter(
        model_user.Users.token == token
    ).first()
    
    if not user:
        return None
    
    # Проверка времени жизни
    current_time = int(time())
    if user.tk_end and user.tk_end < current_time:
        return None
    
    return user

def reg(model, session):
    existing = session.query(model_user.Users).filter(model_user.Users.name == model.name).first()
    if existing:
        return False
    
    try:
        new_usr = model_user.Users(name=model.name, password=model.password)
        session.add(new_usr)
        session.commit()
        return True
    except IntegrityError:
        session.rollback()
        return False
    
def auth(resp, model, session):
    try:
        pers = session.query(model_user.Users).filter(
            model_user.Users.name == model.name
        ).first()
        
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


def get_all(session):
    vals = session.query(model_room.Rooms).all()
    s = []
    for p in vals:
        s.append(p)
    return s

def add(model ,session):
    existing = session.query(model_room.Rooms).filter(model_room.Rooms.name == model.name).first()
    if existing:
        return False
    
    try:
        new_room = model_room.Rooms(name=model.name, places=model.places)
        session.add(new_room)
        session.commit()
        return True
    except IntegrityError:
        session.rollback()
        return False
    
def delete_id(ids, session):
    room = session.query(model_room.Rooms).filter(model_room.Rooms.id == ids).first()
    if not room:
        return False
    try:
        session.delete(room)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        return False