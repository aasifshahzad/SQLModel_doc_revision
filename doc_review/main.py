from typing import Annotated
from fastapi import FastAPI, Depends
from sqlmodel import Session, select


from doc_review.model import Hero
from .db_connect import create_database_table, engine
from .depend import get_session

app = FastAPI(
    title="Hero API",
    description="Hero API used to review SQLModel Documentation",
    version="0.1",
    servers=[
        {
            "url" : "http://localhost:8000",
            "description" : "Development Server"
        }
    ]
)


@app.on_event("startup")
def startup_event():
    create_database_table(engine)
    

@app.get("/")
def get_root():
    return {"Application Status": "Hero API is running!"}

@app.get("/heroes")
def get_heroes(session: Annotated[Session , Depends(get_session)]):
    heroes = session.exec(select(Hero)).all()
    return heroes



# Code below yet to be cover in next class

@app.post("/add_heroes")
def create_hero(hero: Hero, session: Annotated[Session, Depends(get_session)]):
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson", location = "karachi")
    hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador", location = "lahore")
    hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48, location = "islamabad")
    hero_1_to_add = Hero(**hero_1.model_dump(exclude_unset=True))
    hero_2_to_add = Hero(**hero_2.model_dump(exclude_unset=True))
    hero_3_to_add = Hero(**hero_3.model_dump(exclude_unset=True))
    session.add(hero_1_to_add)
    session.add(hero_2_to_add)
    session.add(hero_3_to_add)
    session.commit()
    session.refresh(hero_1_to_add)
    session.refresh(hero_2_to_add)
    session.refresh(hero_3_to_add)
    
    return hero_1_to_add, hero_2_to_add, hero_3_to_add

@app.put("/update_heroes")
def update_heroes(session: Annotated[Session, Depends(get_session)]):
    heroes = session.exec(select(Hero)).all()
    for hero in heroes:
        hero.name = "Hero"
    session.commit()
    return {"message": "Heroes updated successfully"}

@app.delete("/delete_heroes")
def delete_heroes(session: Annotated[Session, Depends(get_session)]):
    heroes = session.exec(select(Hero)).all()
    for hero in heroes:
        session.delete(hero)
    session.commit()
    return {"message": "Heroes deleted successfully"}















    

