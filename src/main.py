from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.routers import rooms, users
from src.database import engine, Base
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created")

    await engine.dispose()
    print("Database connections closed")

async def main():
    app = FastAPI(lifespan=lifespan)
    app.include_router(rooms.router)
    app.include_router(users.router)


if __name__ == "__main__":
    main()
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )