import streamlit as st
from openai import OpenAI
from pypdf import PdfReader  
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
import numpy as np  

# ------------------client instance initialize ------------------
client = OpenAI(
    base_url="https://gen.pollinations.ai/v1", 
    api_key=st.secrets["POLLINATIONS_API_KEY"]
)

# ------ session state for saving data of simple variables ------------
if "messages" not in st.session_state:
     st.session_state.messages = []
if "pdf_chunks" not in st.session_state:
    st.session_state.pdf_chunks = []
if "pdf_vectors" not in st.session_state:
    st.session_state.pdf_vectors = []


for chat in st.session_state.messages:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])


@st.cache_resource
def load_embedding_model():
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")



# -------------side-bar options-----------------
with st.sidebar:
    st.header("Add your PDF")
    st.title("!Attention")
    st.caption("add your file")
    uploaded_file = st.file_uploader("Choose a pdf file", type=["pdf"])
    
    if uploaded_file is not None:
        reader = PdfReader(uploaded_file)
        pdf_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                pdf_text += text + "\n"
                
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = text_splitter.split_text(pdf_text)
        st.session_state.pdf_chunks = chunks
        
        if chunks:
            embedding_model = load_embedding_model()
            vectors = embedding_model.embed_documents(chunks)
            st.session_state.pdf_vectors = vectors
            


user_input = st.chat_input("write something if you want a response from Ai")

if user_input and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # ------------------------ RAG / VECTOR SEARCH LOGIC -------------------------- 
    context = ""
    
   
    if st.session_state.pdf_vectors and st.session_state.pdf_chunks:
        
        query_vector = embedding_model.embed_query(user_input)
        
        
        dot_products = np.dot(st.session_state.pdf_vectors, query_vector)
        matrix_norms = np.linalg.norm(st.session_state.pdf_vectors, axis=1) * np.linalg.norm(query_vector)
        scores = dot_products / matrix_norms
        
        
        top_indexes = np.argsort(scores)[-2:][::-1]
        
       
        retrieved_chunks = [st.session_state.pdf_chunks[idx] for idx in top_indexes]
        context = "\n---\n".join(retrieved_chunks)

    # ------------------------ LLM Response -------------------------- 
    with st.chat_message("assistant"):
        with st.spinner("🤖 Thinking..."):
            try:
                
                messages_for_llm = []
                
                
                if context:
                    system_prompt = f"""You are a helpful assistant. Use the following context extracted from a PDF to answer the user's question accurately. If the answer is not in the context, politely say that you cannot find it in the document. Do not make things up.
                    
                    Context:
                    {context}"""
                    messages_for_llm.append({"role": "system", "content": system_prompt})
                
                
                messages_for_llm.extend(st.session_state.messages)

                response = client.chat.completions.create(
                    model="openai", 
                    messages=messages_for_llm
                )
                ai_response = response.choices[0].message.content
                     
                st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})

            except Exception as e:
                st.error(f"error occured {e}")
