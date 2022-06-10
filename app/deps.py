from typing import Union, Any
from datetime import datetime
from fastapi import Depends, HTTPException, status
from sqlmodel import Session,select
from fastapi.security import OAuth2PasswordBearer
from helpers.utils import (
    ALGORITHM,
    JWT_SECRET_KEY
)

from jose import jwt
from pydantic import ValidationError
from models.auth_schema import TokenPayload, SystemUser
from models.hero import User
from helpers.db import get_db_engine
reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/auth",
    scheme_name="JWT"
)

engine = get_db_engine()
async def get_current_user(token: str = Depends(reuseable_oauth)) -> SystemUser:
    try:
        print("get_current_user")
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    with Session(engine) as session:
        statement = select(User).where(User.email == token_data.sub)
        results = session.exec(statement)
        user = results.first()
    
    
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Could not find user",
            )
        
        return user