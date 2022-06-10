from fastapi import FastAPI
from pydantic import BaseModel
from helpers.db import get_db_engine
from helpers.utils import (
    get_hashed_password,

)
from routes import auth, users, heroes
from sqlmodel import SQLModel 

app = FastAPI(
    title="FastAPI - Hello World",
    description="This is the Hello World of FastAPI.",
    version="1.0.0",
)

engine = get_db_engine()
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(heroes.router)


@app.get("/")
def hello_world():
    return {"Hello": "Wo"}


class Password(BaseModel):
    password: str


@app.post("/hash_password")
def hash_password(password: Password):
    print("start hashing password")
    a = get_hashed_password(password.password)
    print(a)
    return {"password": a}


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

