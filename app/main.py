from fastapi import FastAPI,Depends
from pydantic import BaseModel
from models.hero import Hero, create_db_and_tables,User
from sqlmodel import Field, Session, SQLModel, select  #
from sqlalchemy.engine import URL
from helpers.db import get_db_engine
from helpers.utils import get_hashed_password, verify_password, create_access_token, create_refresh_token
from fastapi.security import OAuth2PasswordBearer
from routes import auth,users
from deps import get_current_user

app = FastAPI(
    title="FastAPI - Hello World",
    description="This is the Hello World of FastAPI.",
    version="1.0.0",
)

engine = get_db_engine()

authenticator = OAuth2PasswordBearer(tokenUrl="auth")

app.include_router(users.router)
app.include_router(auth.router)




# @app.get("/")
# def hello_world():
#     return {"Hello": "Wo"}

class Password(BaseModel):
    password: str

# @app.post("/hash_password")
# def hash_password(password: Password):
#     print("start hashing password")
#     a = get_hashed_password(password.password) 
#     print(a)
#     return {"password": a}
    

@app.get("/heroes",dependencies=[Depends(get_current_user)])
def get_heroes():
    with Session(engine) as session:  #
        statement = select(Hero)  #
        results = session.exec(statement)  #
        heroes = results.fetchall()  #
        return [Hero(name=hero.name, id=hero.id) for hero in heroes]

# @app.get("/heroes/{id}")
# def get_hero(id: int):
#     with Session(engine) as session:
#         statement = select(Hero).where(Hero.id == id)
#         results = session.exec(statement)
#         hero = results.first()
#         return Hero(name=hero.name, id=hero.id, age=hero.age)    

# @app.post("/heroes")
# def create_hero(hero: Hero):
#     with Session(engine) as session:  #
#         session.add(hero)
#         session.commit()
#     return {"message": "Hero created successfully"}


  

@app.on_event("startup")
def on_startup():
    # SQLModel.metadata.create_all(engine)
    create_db_and_tables(engine)