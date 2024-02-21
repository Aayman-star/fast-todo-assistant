""""This file is to create database models"""
import os
from sqlalchemy import create_engine, Column, Integer, String,Boolean
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv,find_dotenv
from sqlmodel import SQLModel, Field, Relationship, Session, select,MetaData
from typing import Optional,Union
import datetime

"""Loading the environment variable"""
load_dotenv(override=True)
dotenv_file = find_dotenv()


DATABASE_URL = os.environ["DATABASE_URL"]
print(DATABASE_URL)

#This is the table for user data
class User(SQLModel,table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    useremail: str
    password:str
    #created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)

#This is the class to create the user from the client side
class UserCreate(SQLModel):
    username: str
    useremail: str
    password:str

class Token(SQLModel):
    access_token: str
    token_type: str
#This is the table for todo data
class Todo_Assistant(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    text: str
    is_complete: bool = False
    user_id: int = Field(foreign_key="user.id") #This is the foreign key to identify the user,the id comes from the user table
    

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



