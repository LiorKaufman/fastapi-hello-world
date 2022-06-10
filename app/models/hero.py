from typing import Optional
from sqlmodel import Field, SQLModel  #


class Hero(SQLModel, table=True):  #
    id: Optional[int] = Field(default=None, primary_key=True)  #
    name: str  #
    secret_name: str  #
    age: Optional[int] = None  #

    class Config:
        schema_extra = {
            "example": {
                "name": "Batman",
                "secret_name": "Bruce Wayne",
                "age": 30,
            }
        }


class User(SQLModel, table=True):  #
    id: Optional[int] = Field(default=None, primary_key=True)  #
    name: str
    email: str
    password: str
