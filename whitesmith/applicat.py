from fastapi import FastAPI
from pydantic import BaseModel
from .db import database
from .models import users
from contextlib import asynccontextmanager

class User(BaseModel):
    name: str
    email: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup event
    await database.connect()
    yield
    # Shutdown event
    await database.disconnect()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "Hello Bud!", "mess" : "It Works "}


@app.post("/users/")
async def create_user(user: User):
    query = users.insert().values(name=user.name, email=user.email)
    user_id = await database.execute(query)
    return {"id": user_id, "name": user.name, "email": user.email}