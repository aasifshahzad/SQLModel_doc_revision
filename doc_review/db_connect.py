from sqlmodel import SQLModel, create_engine
from dotenv import load_dotenv, find_dotenv
import os

_ : bool = load_dotenv(find_dotenv())
CONN_STRING = os.environ.get("CONN_STRING")
print(CONN_STRING)

def create_engine_conn():
    engine = create_engine(CONN_STRING, echo=True)   
    print("Engine created")
    return engine

def create_database_table(engine):
    SQLModel.metadata.create_all(engine)
    print("Table created")


        
engine = create_engine_conn()