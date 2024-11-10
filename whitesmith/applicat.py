from fastapi import FastAPI
from pydantic import BaseModel
from .db import database
from .models import users
from contextlib import asynccontextmanager
from .question_generator import createQuestion, make_fill_blanks

class User(BaseModel):
    name: str
    email: str

class Sentence(BaseModel):
    theme: str
    level: str
    pos: str

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

@app.post("/create_fill_blanks")
async def get_question(sentence: Sentence):
    question = await make_fill_blanks(sentence.theme, sentence.level, sentence.pos, False)
    return {"question" : question}