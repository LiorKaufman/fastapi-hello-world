from models.hero import Hero
from helpers.db import session
from sqlmodel import select 
from fastapi import APIRouter, Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer

router = APIRouter()

authenticator = OAuth2PasswordBearer(tokenUrl="auth")
@router.get("/heroes")
def get_heroes():
    heroes = select(Hero)
    heroes = session.exec(heroes).all()
    return {"heroes": heroes }



@router.get("/heroes/{id}", dependencies=[Depends(authenticator)])
def get_hero_by_id(id: int):
        hero = select(Hero).where(Hero.id == id)
        hero = session.exec(hero).first()
        return {"hero": hero }    

@router.post("/heroes")
def create_hero(hero: Hero):
    hero_ = Hero(name=hero.name, secret_name=hero.secret_name, age=hero.age)
    session.add(hero_)
    session.commit()
    session.refresh(hero_)
    return {"message": "Hero created successfully", "hero": hero_}
