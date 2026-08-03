import streamlit as st
from openai import OpenAI

# ------------------client instance initialize ------------------

client = OpenAI(base_url="https://gen.pollinations.ai/v1", api_key=st.secrets[("POLLINATIONS_API_KEY")]
)


# ------ session state for saving data of simple  variables ------------

if "messages" not in st.session_state:
     st.session_state.messages = []
  

for chat in  st.session_state.messages:
    with st.chat_message(chat["role"]):
      st.markdown(chat["content"])

# -------------side-bar rerun  option-----------------


with  st.sidebar:
    st.header("Rerun option")
    st.title("!Attention")
    st.caption("If you click Rerun button the chat will be reset ")
    if st.button("Rerun"):
        st.session_state.messages= []
        st.rerun()

        


# ------------ user input -------------------



user_input = st.chat_input(
    "write something if you want a response from Ai",
    submit_mode= "disable"

 )

if user_input and user_input.strip():
    st.session_state.messages.append({"role":"user","content":user_input})
    st.chat_message("user").write(user_input)


    # ------------------------ LLM Response -------------------------- 


    with st.spinner("🤖 Thinking..."):
        try:
            response = client.chat.completions.create(model="openai", messages=st.session_state.messages)
            ai_response= response.choices[0].message.content
                 
            st.chat_message("assistant").write(ai_response)
            st.session_state.messages.append({"role":"assistant","content":ai_response})
            st.rerun()

        except Exception as e:
            st.error(f"error occured {e}")
       
