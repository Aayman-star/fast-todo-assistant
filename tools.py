"""
This file contains defintions and descriptions of all the functions needed by the open ai assistant to communicate with the back-end
"""

import json
import requests
from typing import Any,List
from database import TodoCreate,TodoRead
"""
Defining the functions
"""

BASE_URL = "http://127.0.0.1:8000"

def get_todos()->List[TodoRead]:
    """
    This function to get the todos
    """
    try:
        response = requests.get(f"{BASE_URL}/")
        return json.dumps(response.json())
    except:
        return json.dumps({"response": "Apologies,I could not access the requested information"})

def create_todo(todo:str)->dict:
    """
    This function to create the todo
    """
    try:
        response = requests.post(f"{BASE_URL}/create-todo",json={"text":todo})
        return json.dumps(response.json())
    except:
        return json.dumps({"response": "There was problem with creating the Todo"})

def delete_todo(id:int)->dict:
    """
    This function to delete the todo
    """
    try:
        response = requests.delete(f"{BASE_URL}/del/{id}")
        return json.dumps(response.json())
    except:
        return json.dumps({"response": "There was problem with deleting the Todo"})

def check_todo(id:int)->dict:
    """
    This function marks the todo as complete by changing the is_complete value from false to true or from true to false
    """
    try:
        response = requests.put(f"{BASE_URL}/check-todo/{id}")
        return json.dumps(response.json())
    except:
        return json.dumps({"response": "There was problem with checking the Todo"})

def update_todo(id:int,todo:str)->dict:
    """
    This function updates the text of the todo item
    """
    try:
        response = requests.put(f"{BASE_URL}/update-todo/{id}", json={"id":id,"text":todo})
        return json.dumps(response.json())
    except:
        return json.dumps({"response": "There was problem with updating the Todo"})

def get_complete_todos()->List[TodoRead]:
     """
     This functions returns the list of complete todos
     """
     try:
         response = requests.get(f"{BASE_URL}/complete-todos")
         return json.dumps(response.json())
     except:
          return json.dumps({"response": "Apologies, I could not access the requested information"})

def get_incomplete_todos()->List[TodoRead]:
    """
    This functions returns the list of incomplete todos
    """
    try:
        response = requests.get(f"{BASE_URL}/incomplete-todos")
        return json.dumps(response.json())
    except:
        return json.dumps({"response": "Apologies, I could not access the requested information"})

def clear_todos()->dict:
    """
    This function is to clear the list of todos,erase all the todos from the database
    """
    try:
        response = requests.delete(f"{BASE_URL}/delete-all")
        return json.dumps(response.json())
    except:
        return json.dumps({"response": "There was problem with clearing the Todos"})
          
"""
Mapping available functions
"""
available_functions = {
    "get_todos":get_todos,
    "create_todo":create_todo,
    "delete_todo":delete_todo,
    "check_todo":check_todo,
    "update_todo":update_todo,
    "get_complete_todos":get_complete_todos,
    "get_incomplete_todos":get_incomplete_todos,
    "clear_todos":clear_todos

}

function_descriptions = [
        {

            "type": "function",
            "function": {
                "name": "get_todos",
                "description": "Get the list of todos from the database",
                "parameters": {
                     "type": "object",
                     "properties":{}
                   
                },
                "required":[]
                
           
            }
        },
        {
            "type": "function",
            "function": {
                "name": "create_todo",
                "description": "Creating a todo and storing in the database",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "todo": {"type": "string", "description": "The text of the todo items"},
                       

                    },
                    "required": ["todo"]
                }
            }
        },
        {
             "type": "function",	
             "function": {
                  "name":"delete_todo",
                  "description":"Deleting a todo from the database based on the id of the todo item",
                  "parameters":{
                       "type":"object",
                       "properties":{
                            "id":{"type":"integer","description":"The id of the todo item to delete"	}
                       },
                       "required":["id"]
                  }
             }
        },
               {
             "type": "function",	
             "function": {
                  "name":"check_todo",
                  "description":" This function marks the todo as complete by changing the is_complete value from false to true or from true to false",
                  "parameters":{
                       "type":"object",
                       "properties":{
                            "id":{"type":"integer","description":"The id of the todo item to mark as done"	}
                       },
                       "required":["id"]
                  }
             }
        },
                       {
             "type": "function",	
             "function": {
                  "name":"update_todo",
                  "description":"This function updates the text of the todo item",
                  "parameters":{
                       "type":"object",
                       "properties":{
                            "id":{"type":"integer","description":"The id of the todo item to update"},
                            "todo":{"type":"string","description":"The new text of the todo item"}
                       },
                       "required":["id","todo"]
                  }
             }
        },
        { 
             "type": "function",
            "function": {
                "name": "get_complete_todos",
                "description": "Get the list of checked todos from the database",
                "parameters": {
                     "type": "object",
                     "properties":{}
                   
                },
                "required":[]
                
           
            }
        },
            { 
             "type": "function",
            "function": {
                "name": "get_incomplete_todos",
                "description": "Get the list of todos from the database which are marked as incomplete",
                "parameters": {
                     "type": "object",
                     "properties":{}
                   
                },
                "required":[]
                
           
            }
        },
             {

            "type": "function",
            "function": {
                "name": "clear_todos",
                "description": "Erase all  todos from the database",
                "parameters": {
                     "type": "object",
                     "properties":{}
                   
                },
                "required":[]
                
           
            }
        }
]
