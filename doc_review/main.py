from typing import Annotated
from fastapi import FastAPI, Depends
from sqlmodel import Session, select


from doc_review.model import Hero, HeroUpdate
from .db_connect import create_database_table, engine
from .depend import get_session
from fastapi import HTTPException

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

# @app.post("/add_heroes")
# def create_hero(hero: Hero, session: Annotated[Session, Depends(get_session)]):
    hero_1 = Hero(name="Iron-Man", secret_name="Tony Stark", age=28, location = "lahore" )
    hero_2 = Hero(name="Nadeem", secret_name="Pedro Parqueador", location = "lahore")
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

@app.post("/add_heroes")
def create_hero(hero: Hero, session: Annotated[Session, Depends(get_session)]):
    hero_to_add = Hero(**hero.model_dump(exclude_unset=True))
    session.add(hero_to_add)
    session.commit()
    session.refresh(hero_to_add)
    return hero_to_add, "Hero added successfully"


@app.patch("/update_heroes/{name}")
def update_heroes(name : str, hero_update : HeroUpdate, session: Annotated[Session, Depends(get_session)]):
    hero_to_update = session.exec(select(Hero).where(Hero.name == name)).first()
    if not name:
        # return {"message": "Hero not found"}
        raise HTTPException(status_code=404, detail="Hero not found")
    print("Hero in database", hero_to_update)
    print("Hero from client", hero_update)
    
    hero_to_update_dict = hero_update.model_dump(exclude_unset=True)
    print("Hero to update dict", hero_to_update_dict)
    
    for key, value in hero_to_update_dict.items():
        setattr(hero_to_update, key, value) 
    
    print("Hero after update", hero_to_update)
    session.commit()
    session.refresh(hero_to_update)
    return hero_to_update, "Hero updated successfully"  

# @app.put("/update_heroes/{name}")
# def update_heroes(name : str, hero_update : HeroUpdate, session: Annotated[Session, Depends(get_session)]): 
#     full_update = session.exec(select(Hero).where(Hero.name == name)).first()
#     if not name:    
#         # return {"message": "Hero not found"}
#         raise HTTPException(status_code=404, detail="Hero not found")
#     if full_update.name:
#         full_update.name = hero_update.name
#     if full_update.age:
#         full_update.age = hero_update.age
#     if full_update.location:
#         full_update.location = hero_update.location
#     if full_update.name:
#         full_update.name = hero_update.name
    
#     session.add(full_update)
#     session.commit()
#     session.refresh(full_update)
#     return full_update, "Hero updated successfully"
    
@app.delete("/delete_heroes_all")
def delete_heroes(session: Annotated[Session, Depends(get_session)]):
    heroes = session.exec(select(Hero)).all()
    for hero in heroes:
        session.delete(hero)
    session.commit()
    return {"message": "Heroes deleted successfully"}

@app.delete("/delete_heroes/{name}")
def delete_heroes(name : str , session: Annotated[Session, Depends(get_session)]):
    hero = session.exec(select(Hero).where(Hero.name == name)).first()
    session.delete(hero)
    session.commit()
    return {"message": "Hero deleted successfully"}














    

