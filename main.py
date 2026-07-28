from google import genai
import streamlit as st
import os 
from dotenv import load_dotenv
load_dotenv() 
GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
title = st.title("welcome to my chatbot")
user_input = st.chat_input("write  something here")

if user_input:
    client = genai.Client(api_key=GEMINI_API_KEY)
    interactions = client.interactions.create(
     model="gemini-3.6-flash",
    input=user_input,
)
    st.write(interactions.output_text)




   


