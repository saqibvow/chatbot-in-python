import streamlit as st
from openai import OpenAI

user_input = st.chat_input("write something if you want a response from Ai")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for chat in st.session_state.chat_history:
    st.write(chat["content"])
if user_input:
    client = OpenAI(base_url="https://gen.pollinations.ai/v1", api_key="sk_UtdfC8O4gpwGAWDGD9Af2btUJzZanlPV")
    response = client.chat.completions.create(model="openai", messages=[{"role": "user", "content": user_input}])
    output = st.text(response.choices[0].message.content)
    st.session_state.chat_history.append(user_input)
    print(response.choices[0].message.content,flush=True)