from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
import models 


DB_ROOM_URL = "sqlite:///./db/sql_rooms.db"
room_engine = create_engine(DB_ROOM_URL, connect_args={"check_same_thread": False})
SessionRoom = sessionmaker(autoflush=False, bind=room_engine)


DB_USER_URL = "sqlite:///./db/sql_users.db"
user_engine = create_engine(DB_USER_URL, connect_args={"check_same_thread": False})
SessionUser = sessionmaker(autoflush=False, bind=user_engine)

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


def get_all(session):
    vals = session.query(models.Rooms).all()
    s = []
    for p in vals:
        s.append(p)
    return s

def add(model ,session):
    existing = session.query(models.Rooms).filter(models.Rooms.name == model.name).first()
    if existing:
        return False
    
    try:
        new_room = models.Rooms(name=model.name, places=model.places)
        session.add(new_room)
        session.commit()
        return True
    except IntegrityError:
        session.rollback()
        return False
    
def delete_id(ids, session):
    room = session.query(models.Rooms).filter(models.Rooms.id == ids).first()
    if not room:
        return False
    try:
        session.delete(room)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        return False