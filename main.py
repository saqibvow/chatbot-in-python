import streamlit as st
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

st.title(" Welcome to my Chatbot")


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["text"])


user_input = st.chat_input("Write something here...")

if user_input:
    
    with st.chat_message("user"):
        st.write(user_input)
    
    
    st.session_state.chat_history.append({"role": "user", "text": user_input})
    
    
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    with st.spinner("AI is thinking..."):
        interactions = client.interactions.create(
                model="gemini-3.6-flash",
                input=user_input, 
            )
    bot_response = interactions.output_text
     
     
    with st.chat_message("assistant"):
         st.write(bot_response)
         
         st.session_state.chat_history.append({"role": "assistant", "text": bot_response})
