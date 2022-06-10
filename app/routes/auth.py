from fastapi.security import OAuth2PasswordRequestForm
from models.hero import User
from helpers.utils import (
    get_hashed_password,
    create_access_token,
    create_refresh_token,
    verify_password,
)
from uuid import uuid4
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Field, Session, SQLModel, select
from helpers.db import get_db_engine


router = APIRouter()


class Token(BaseModel):
    access_token: str
    refresh_token: str


engine = get_db_engine()


@router.post(
    "/auth",
    summary="Create access and refresh tokens for user",
    response_model=Token,
    include_in_schema=False,
)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    with Session(engine) as session:
        statement = select(User).where(User.email == form_data.username)
        results = session.exec(statement)
        user = results.first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect email or password",
            )

    hashed_pass = user.password
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    access_token = create_access_token(user.email) 
    refresh_token = create_refresh_token(user.email)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }
