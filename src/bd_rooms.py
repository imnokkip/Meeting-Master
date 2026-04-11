from sqlalchemy.orm import sessionmaker
import models
class Rooms_bd():
    def __init__(self):
        global Session_room
        DB_ROOM_URL = "sqlite:///./db/sql_rooms.db"
        room_engine = models.create_engine(DB_ROOM_URL, connect_args={"check_same_thread": False})
        models.Base.metadata.create_all(bind=room_engine)
        Session_room = sessionmaker(autoflush=False, bind=room_engine)


    def get_bd_room():
        db = Session_room()
        try:
            yield db
        finally:
            db.close()
