""""This file is to create database models"""
import os
from sqlalchemy import create_engine, Column, Integer, String,Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv,find_dotenv
from sqlmodel import SQLModel, Field, Relationship, Session, select,MetaData
from typing import Optional,Union

"""Loading the environment variable"""
load_dotenv(override=True)
dotenv_file = find_dotenv()


DATABASE_URL = os.environ["DATABASE_URL"]
print(DATABASE_URL)


class Todo_Assistant(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    text: str
    is_complete: bool = False
    

class TodoCreate(SQLModel):
    text: str
    is_complete: bool = False

class TodoRead(SQLModel):
    id: int
    text: str
    is_complete: bool 

class TodoUpdate(SQLModel):
    id:int
    text: str
    is_complete: Optional[bool] = False


    

engine = create_engine(DATABASE_URL, echo=True)
def create_table():
    SQLModel.metadata.create_all(engine)



