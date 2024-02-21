"""This file is to integrate the openai assisant api"""

from fastapi.datastructures import FormData
import streamlit as st
from model import OpenAIAssistant,MessageItem
from auth import create_user,login_for_access_token
import requests
import json

url = "http://127.0.0.1:8000/auth"
def todo_assistant():
    st.title("Todo Assistant")

    if "todo_assistant" not in st.session_state:
        st.session_state.todo_assistant = OpenAIAssistant(
            name = "Todo Assistant",
            instructions = """
                        Act as a todo assistant by performing all the CRUD(Create,Read,Update,Delete) operations on the todos
                        in the database,by accessing the api 
                            """
        )

    for m in st.session_state.todo_assistant.getMessages():
        with st.chat_message(m.role):
            st.markdown(m.content)


    if prompt := st.chat_input("Please Ask a Question"):
        st.session_state.todo_assistant.ask_question(prompt)
        with st.chat_message("user"):
            st.markdown(prompt)

        if(st.session_state.todo_assistant.is_completed()):
            response: MessageItem = st.session_state.todo_assistant.get_response()
            with st.chat_message(response.role):
                st.markdown(response.content)

#Creating the login/signup page
st.title("Welcome to the todo assistant")
choice = st.selectbox("Login or SignUp", ["Login", "SignUp"])
# Create an empty container
placeholder = st.empty()

# Insert a form in the container with placeholder.form("login"):

if choice == "Login":
    with placeholder.form("Login"):
        st.markdown("#### Enter your credentials")
        username = st.text_input("Username") 
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

    if submit:
            try:
                response = requests.post(f"{url}/token", data={'username': username, 'password': password},  
                                        )
                if response.status_code == 200:
                   token_info = response.json()
                #    st.write(f"Access Token: {token_info['access_token']}")
                #    st.write(f"Token Type: {token_info['token_type']}")
                    
    
                   st.success("Login successful")
                   todo_assistant()
        
        # Import and call your app function here
       
            except:
                st.error("Login failed")
else:
    with placeholder.form("SignUp"):
        st.markdown("#### Enter your credentials")
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("SignUp")
    if submit:
        try:
            response = requests.post(f"{url}/", data=json.dumps({'username': username, 'email': email, 'password': password}))
            placeholder.empty()
            st.success("Signup successful")
            todo_assistant()
        except:
            st.error("Signup failed")



