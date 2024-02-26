"""This file is to integrate the openai assisant api"""


import streamlit as st
from model import OpenAIAssistant,MessageItem

#url = "http://127.0.0.1:8000/auth"

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






