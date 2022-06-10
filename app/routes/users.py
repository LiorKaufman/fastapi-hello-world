from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Query
from fastapi.security.oauth2 import OAuth2PasswordBearer
from sqlmodel import Field, Session, SQLModel, select
from models.hero import User
from helpers.db import session

router = APIRouter(prefix="/users")

authenticator = OAuth2PasswordBearer(tokenUrl="auth")


@router.get("/users", dependencies=[Depends(authenticator)])
def get_users():
    print("get_users")
    with session:
        statement = select(User)
        results = session.exec(statement)
        users = results.fetchall()
        return [User(name=user.name, id=user.id) for user in users]
