import streamlit as st
import tempfile
import os
import requests
from PyPDF2 import PdfReader

# ✅ Initialize Streamlit app
st.set_page_config(page_title="PDF RAG Assistant", page_icon="📘", layout="wide")

# ✅ Define helper to initialize Streamlit session state
def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "pdf_text" not in st.session_state:
        st.session_state["pdf_text"] = ""
    if "model_choice" not in st.session_state:
        st.session_state["model_choice"] = "llama-3.1-8b-instant"

initialize_session_state()  # ✅ Fix: define and call here safely

# ✅ Function to extract text from uploaded PDF
def extract_pdf_text(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text.strip()

# ✅ Function to query Groq API
def query_groq(api_key, model, prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data["choices"][0]["message"]["content"]
    else:
        st.error(f"Groq API error: {response.status_code} - {response.text}")
        return None

# ✅ Streamlit UI layout
st.title("📚 PDF RAG Assistant")
st.write("Upload a PDF and ask questions about its content using Groq LLMs.")

# Sidebar
st.sidebar.header("Configuration")
groq_api_key = st.sidebar.text_input("🔑 Enter your Groq API Key", type="password")
model_choice = st.sidebar.selectbox(
    "🧠 Choose a model",
 [
    "mixtral-8x7b-32768",
    "llama-3.1-8b-instant",
    "gemma-7b-it",
    "llama-3.3-70b-versatile"
]
)
st.session_state["model_choice"] = model_choice

# File uploader
uploaded_pdf = st.file_uploader("📄 Upload your PDF", type=["pdf"])

if uploaded_pdf:
    st.success("✅ PDF uploaded successfully!")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_pdf.read())
        temp_file_path = temp_file.name

    pdf_text = extract_pdf_text(temp_file_path)
    st.session_state["pdf_text"] = pdf_text

    with st.expander("📘 View Extracted Text"):
        st.text_area("Extracted PDF Text", pdf_text, height=250)

# Question input
st.subheader("💬 Ask a question about your PDF")
question = st.text_input("Type your question:")

if st.button("🔍 Get Answer"):
    if not groq_api_key:
        st.error("Please enter your Groq API key in the sidebar.")
    elif not uploaded_pdf:
        st.error("Please upload a PDF first.")
    elif not question.strip():
        st.error("Please enter a question.")
    else:
        context = st.session_state["pdf_text"][:8000]  # limit context for token safety
        full_prompt = f"Answer based on the following PDF content:\n\n{context}\n\nQuestion: {question}"
        answer = query_groq(groq_api_key, model_choice, full_prompt)
        if answer:
            st.session_state["messages"].append({"question": question, "answer": answer})
            st.success("✅ Answer received!")
            st.write(answer)

# Chat history display
if st.session_state["messages"]:
    st.subheader("🧾 Chat History")
    for i, chat in enumerate(st.session_state["messages"], 1):
        st.markdown(f"*Q{i}:* {chat['question']}")
        st.markdown(f"*A{i}:* {chat['answer']}")
        st.markdown("---")

