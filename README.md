#  PDF RAG Chatbot

An AI-powered chatbot built with Streamlit that allows you to upload a PDF document and ask questions directly from its content using RAG (Retrieval-Augmented Generation) and Hugging Face Embeddings.

##  How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/saqibvow/chatbot-in-python.git
cd chatbot-in-python
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup API Keys
Create a folder named `.streamlit` and a file inside it named `secrets.toml`:
```toml
 "your_actual_api_key_here"
```

### 4. Run the App
```bash
python -m streamlit run main.py
```
