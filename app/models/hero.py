from typing import Optional
from helpers.db import get_db_engine   

from sqlmodel import Field, SQLModel  # 


class Hero(SQLModel, table=True):  # 
    id: Optional[int] = Field(default=None, primary_key=True)  # 
    name: str  # 
    secret_name: str  # 
    age: Optional[int] = None  # 


class User(SQLModel, table=True):  #
    id: Optional[int] = Field(default=None, primary_key=True)  #
    name: str
    email: str
    password: str



def create_db_and_tables(engine):  # 
    SQLModel.metadata.create_all(engine)  # 


