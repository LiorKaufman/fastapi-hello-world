from datetime import datetime
from functools import lru_cache
from typing import List
from sqlalchemy.engine.base import Engine

from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Query
from fastapi.security.oauth2 import OAuth2PasswordBearer
from sqlmodel import Field, Session, SQLModel, select
from helpers.db import get_db_engine
from models.hero import User
from deps import get_current_user
router = APIRouter(prefix="/users")

authenticator = OAuth2PasswordBearer(tokenUrl="auth")

engine = get_db_engine()
@router.get("/users", dependencies=[Depends(get_current_user)])
def get_users():
    print("get_users")    
    with Session(engine) as session:
        statement = select(User)
        results = session.exec(statement)
        users = results.fetchall()
        return [User(name=user.name, id=user.id) for user in users]  