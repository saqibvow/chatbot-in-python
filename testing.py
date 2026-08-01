import streamlit as st
from openai import OpenAI

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Chatbot")
st.caption("Powered by Pollinations AI")

# ---------------- CLIENT ----------------

client = OpenAI(
    base_url="https://gen.pollinations.ai/v1",
    api_key="YOUR_NEW_API_KEY"
)
  

# ---------------- SESSION ----------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.header("Settings")

    if st.button("🗑 Clear Chat"):

        st.session_state.messages = []

        st.rerun()

# ---------------- SHOW CHAT ----------------

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
    
            st.markdown(message["content"])
    

    
# ---------------- USER INPUT ----------------

prompt = st.chat_input("Ask me anything...")

if prompt:

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # Display user message
    with st.chat_message("user"):

        st.markdown(prompt)

    # Build messages

    api_messages = [

        {
            "role": "system",
            "content": "You are a friendly AI assistant."
        }

    ] + st.session_state.messages

    try:

        with st.chat_message("assistant"):

            with st.spinner("🤖 Thinking..."):

                response = client.chat.completions.create(

                    model="openai",

                    messages=api_messages

                )

                ai_response = response.choices[0].message.content

                st.markdown(ai_response)

        st.session_state.messages.append(

            {
                "role": "assistant",
                "content": ai_response
            }

        )

    except Exception as e:

        st.error(f"Error: {e}")