from app.models.hero import User
from app.helpers.utils import (
    create_access_token,
    create_refresh_token,
    verify_password,
)
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, status
from sqlmodel import SQLModel, select
from app.helpers.db import session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi import Depends
router = APIRouter()


class Token(BaseModel):
    access_token: str
    refresh_token: str


class UserLogin(SQLModel):
    username: str
    password: str


@router.post(
    "/auth",
    summary="Create access and refresh tokens for user",
    response_model=Token,
    include_in_schema=False,
)
async def login(form_data:  OAuth2PasswordRequestForm = Depends()):
    user = select(User).where(User.email == form_data.username)
    user = session.exec(user).first()
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
    return {"access_token": access_token, "refresh_token": refresh_token}
