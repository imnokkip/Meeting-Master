from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import select
from src.models.model import Rooms, Users, Base
from time import time
from src import tokenizer
import os
from dotenv import load_dotenv

load_dotenv()

PWD = os.getenv("pass")
USR = os.getenv("name")

DB_URL = os.getenv("DATABASE_URL")
engine = create_async_engine(DB_URL, pool_size=20, max_overflow=10, echo=True)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        finally:
            await db.close()

async def check_token(session_user: AsyncSession, token: str):
    if not token:
        return False
    
    user = (await session_user.execute(
        select(Users).where(Users.token == token)
    )).scalar_one_or_none()
    
    if not user:
        return False
    
    current_time = int(time())
    if user.tk_end and user.tk_end < current_time:
        return False
    
    return True

async def get_current_user_from_token(token: str, db_user: AsyncSession):
    user = (await db_user.execute(
        select(Users).where(Users.token == token)
    )).scalar_one_or_none()
    
    if not user:
        return None
    
    current_time = int(time())
    if user.tk_end and user.tk_end < current_time:
        return None
    
    return user

async def reg(model, session: AsyncSession):
    existing = (await session.execute(
        select(Users).where(Users.name == model.name)
    )).scalar_one_or_none()
    
    if existing:
        return False
    
    try:
        new_usr = Users(name=model.name, password=model.password)
        session.add(new_usr)
        await session.commit()
        return True
    except IntegrityError:
        await session.rollback()
        return False

async def auth(resp, model, session: AsyncSession):
    print("start!")
    try:
        pers = (await session.execute(
            select(Users).where(Users.name == model.name)
        )).scalar_one_or_none()
        
        if not pers or pers.password != model.password:
            
            return False
            
        tok = str(tokenizer.generate(pers.name, pers.password))
        
        pers.token = tok
        pers.tk_end = int(time()) + 60
        print('set cook')
        resp.set_cookie(key="session_token", value=tok, httponly=True)
        await session.commit()
        
        return True
    except Exception as e:
        print('no')
        await session.rollback()
        return False

async def get_all(session: AsyncSession):
    vals = (await session.execute(select(Rooms))).scalars().all()
    return vals

async def add(model, session: AsyncSession):
    existing = (await session.execute(
        select(Rooms).where(Rooms.name == model.name)
    )).scalar_one_or_none()
    
    if existing:
        return False
    
    try:
        new_room = Rooms(name=model.name, places=model.places)
        session.add(new_room)
        await session.commit()
        return True
    except IntegrityError:
        await session.rollback()
        return False

async def delete_id(ids: int, session: AsyncSession):
    room = (await session.execute(
        select(Rooms).where(Rooms.id == ids)
    )).scalar_one_or_none()
    
    if not room:
        return False
    
    try:
        session.delete(room)
        await session.commit()
        return True
    except Exception as e:
        await session.rollback()
        return False