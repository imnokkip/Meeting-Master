from fastapi import FastAPI
from routers import rooms, users
from database import init_db
import uvicorn

app = FastAPI()
app.include_router(rooms.router)
app.include_router(users.router)

if __name__ == "__main__":
    init_db()
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)