"""
This file to create the model for the todo gpt assistant

"""
import os
import time
import json
import requests
from typing import Any,List
from dotenv import load_dotenv, find_dotenv
from database import TodoCreate,TodoRead
from openai import OpenAI
from openai.types.beta import Assistant
from openai.types.beta.thread import Thread
from openai.types.beta.threads.thread_message import ThreadMessage
from openai.types.beta.threads.run import Run
from tools import available_functions,function_descriptions

"""
#Importing the keys
"""
_: bool = load_dotenv(find_dotenv())

API_KEY = os.environ["OPENAI_API_KEY"]


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
            tools = function_descriptions,
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
