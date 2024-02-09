""""This file is for the backend"""

import select
from fastapi import FastAPI,Body,Depends,HTTPException
from sqlalchemy.orm import Session
from database import engine,Todo_Assistant as TA,TodoCreate,TodoRead,TodoUpdate
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
import uvicorn
from sqlmodel import Session, delete,select
from typing import List


app: FastAPI = FastAPI()


# Dependency
def get_session():
    with Session(engine) as session:
        yield session


@app.get("/api/python")
def hello_world():
    return {"message": "Hello World"}



@app.get("/",response_model=List[TodoRead])
def read_todos(*,session:Session=Depends(get_session)):
    """Get all Todos"""
    todos = session.exec(select(TA).order_by(TA.id)).all()
    if todos is None:
        raise HTTPException(status_code=404, detail="No todos found")
        #return {"message":"No todos found"	}
    return todos


@app.get("/todo/{todo_id}",response_model=TodoRead)
def get_todo(*,session:Session = Depends(get_session),todo_id:int):
    """Get a single todo from the database"""
    todo = session.get(TA, todo_id)  # Get the todo item from the database
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.post("/create-todo",response_model=TodoRead)
def create_todo(*,session:Session = Depends(get_session),todo:TodoCreate):
    """Creating and storing a todo item in the database"""
    todo_item = TA.model_validate(todo)
    session.add(todo_item)
    session.commit()
    session.refresh(todo_item)
    return todo_item

@app.get("/complete-todos",response_model=List[TodoRead])
def get_complete_todos(*,session:Session = Depends(get_session)):
    """Get all complete todos"""
    todos = session.exec(select(TA).where(TA.is_complete == True)).all()
    if todos is None:
        raise HTTPException(status_code=404, detail="No todos found")
    return todos

@app.get("/incomplete-todos",response_model=List[TodoRead])
def get_complete_todos(*,session:Session = Depends(get_session)):
    """Get all complete todos"""
    todos = session.exec(select(TA).where(TA.is_complete == False)).all()
    if todos is None:
        raise HTTPException(status_code=404, detail="No todos found")
    return todos

@app.put("/check-todo/{task_id}")
def check_task(*,session:Session = Depends(get_session),task_id:int):
    """Check a task as complete"""
    db_todo = session.get(TA, task_id)  # Get the todo item from the database
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db_todo.is_complete = not db_todo.is_complete
    session.add(db_todo)  # Add the updated todo to the session
    session.commit()
    session.refresh(db_todo)
    return db_todo

@app.put("/update-todo/{task_id}",response_model=TodoRead)
def update_todo(*,session:Session = Depends(get_session),task_id:int,todo:TodoUpdate):
    print(task_id,todo)
    """Update Todo Description"""
    db_todo = session.get(TA,task_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo_data = todo.model_dump(exclude_unset=True)
    print(todo_data)
    for key, value in todo_data.items():
        setattr(db_todo, key, value)
    print(db_todo)
    session.add(db_todo)  # Add the updated todo to the session 
    session.commit()
    session.refresh(db_todo)
    return db_todo

@app.delete("/del/{todo_id}")
def delete_todo(*,session:Session = Depends(get_session),todo_id:int):
    """Delete a todo from the database"""
    print(f"This is the id {todo_id}")
    todo = session.get(TA,todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    session.delete(todo)
    session.commit()
    return {"message": "Todo deleted successfully"}

@app.delete("/delete-all")
def delete_all(*,session:Session = Depends(get_session)):
    """Delete all todos from the database"""
    result = session.exec(delete(TA))
    session.commit()
    return {"message": f"{result.rowcount} todos deleted successfully"}



if __name__ == "__main__":
    uvicorn.run("app:app", reload=True)

