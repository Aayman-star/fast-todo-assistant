"""
This file to create the model for the todo gpt assistant

"""
from openai import OpenAI
from openai.types.beta import Assistant
from openai.types.beta.thread import Thread
from openai.types.beta.threads.thread_message import ThreadMessage
from openai.types.beta.threads.run import Run
import json
from dotenv import load_dotenv, find_dotenv
import os
import time
import requests
from typing import Any,List
from database import TodoCreate,TodoRead

"""
#Importing the keys
"""
_: bool = load_dotenv(find_dotenv())

API_KEY = os.environ["OPENAI_API_KEY"]

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

}

"""
#The class for message 
"""
class MessageItem:
      def __init__(self, role: str, content: str | Any):
        self.role: str = role
        self.content: str | Any = content

class OpenAIAssistant:
    def __init__(self,name:str,instructions:str,model:str="gpt-3.5-turbo-1106"):
        self.name:str= name;
        self.instructions:str = instructions;
        self.model :str = model;
        load_dotenv(find_dotenv());
        self.client :OpenAI = OpenAI();
        self.assistant : Assistant = self.client.beta.assistants.create(
            name=self.name,
            instructions= self.instructions,
            tools = [
               
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
        
        
 



  
            ],
            model = self.model
            )
        """
        #1Thread being initialized 
        """
        self.thread :Thread = self.client.beta.threads.create()
        """
        #2.Creating a list of messages to keep track of the conversation between the user and the assistant
        """
        self.messages :list[MessageItem] = [];

        """
        #This will return the name of the assistant
        """
    def get_name(self):
        return self.name
        """
        #This will return the instrctions
        """
    def get_instructions(self):
        return self.instructions
        
    def ask_question(self,message:str):
        current_thread : ThreadMessage = self.client.beta.threads.messages.create(
            thread_id = self.thread.id,
            role = "user",
            content = message
            )

        self.latest_run :Run = self.client.beta.threads.runs.create(
                thread_id = self.thread.id,
                assistant_id = self.assistant.id,
                instructions = self.instructions
            )

        self.addMessage(MessageItem(role="user", content=message))

        """
        #This function will check the status of the run 
        """
    def is_completed(self)->bool:
            print("Status",self.latest_run.status)
            while True:
                # print("Going to sleep")
                # time.sleep(1)
                self.latest_run : Run = self.client.beta.threads.runs.retrieve(
                    thread_id = self.thread.id,
                    run_id = self.latest_run.id
                )
                print("Latest Status: ", self.latest_run.status)
                if self.latest_run.status == "requires_action":
                    print("Latest Status: ", self.latest_run.status)
                    if self.latest_run.required_action.submit_tool_outputs and self.latest_run.required_action.submit_tool_outputs.tool_calls:
                        print("tool calls present")
                        toolCalls = self.latest_run.required_action.submit_tool_outputs.tool_calls
                        tool_outputs = [];
                        for toolcall in toolCalls:
                             function_name = toolcall.function.name
                             function_args = json.loads(toolcall.function.arguments)
                             
                             if function_name in available_functions:
                                 function_to_call = available_functions[function_name]
                                 print("function to call ====================",function_to_call)
                                 output = function_to_call(**function_args)
                                 print("output =====================", output)
                                 tool_outputs.append({
                                                "tool_call_id": toolcall.id,
                                                "output": output,
                                            })
                                 # Submit tool outputs and update the run
                        self.client.beta.threads.runs.submit_tool_outputs(
                            thread_id = self.thread.id,
                            run_id=self.latest_run.id,
                            tool_outputs=tool_outputs
                                     )
                                 
                           
                           
                elif self.latest_run.status == "completed": 
                    messages = self.client.beta.threads.messages.list(
                        thread_id = self.thread.id
                    )

                    break

                elif self.latest_run.status == "failed":
                    print("Run Failed")
                    break
                
                elif self.latest_run.status in ["in_progress","queued"]:
                      print(f"Run is {self.latest_run.status}. Waiting...")
                      time.sleep(5)

            return True
        
    def get_response(self)->MessageItem:
            messages = self.client.beta.threads.messages.list(thread_id = self.thread.id)
            print("Answer",messages.data[0])

            answer = MessageItem(messages.data[0].role, messages.data[0].content[0].text.value)
            self.addMessage(answer)
            return answer
        
    def getMessages(self)->list[MessageItem]:
            return self.messages

    def addMessage(self, message: MessageItem)->None: 
            self.messages.append(message)
