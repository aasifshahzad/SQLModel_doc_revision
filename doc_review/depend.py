from sqlmodel import Session
from .db_connect import engine

def get_session():
    with Session(engine) as session:
        print("session created")
        yield session