from fastapi import FastAPI
from .db import database
from .models import users
from contextlib import asynccontextmanager



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
async def create_user(name: str, email: str):
    query = users.insert().values(name=name, email=email)
    user_id = await database.execute(query)
    return {"id": user_id, "name": name, "email": email}