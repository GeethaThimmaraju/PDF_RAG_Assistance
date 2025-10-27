📚 PDF RAG Assistant

An interactive Streamlit app that lets you upload PDFs and ask questions about their contents — powered by Groq LLMs such as LLaMA 3, Mixtral, Gemma, and more.
This app extracts text from your uploaded PDF, sends your query + context to the Groq API, and returns intelligent answers.

🚀 Features

✅ Upload any PDF and extract its text automatically
✅ Ask questions about the document content
✅ Choose from multiple Groq models
✅ Simple, clean Streamlit UI
✅ Keeps chat history in session
✅ Runs fully locally with just your Groq API key

🧠 Tech Stack
Component	Description
Python	Core language
Streamlit	Web UI framework
PyPDF2	Extract text from PDFs
Requests	For Groq API calls
Groq API	LLM inference backend
🧩 Project Structure
📁 IntelliChat_Gemini/
│
├── app.py                 # Main Streamlit app
├── utils.py               # (Optional helper functions if added)
├── requirements.txt       # Dependencies
└── README.md              # Documentation

⚙️ Installation

Clone the repository

git clone https://github.com/<your-username>/pdf-rag-assistant.git
cd pdf-rag-assistant


Create a virtual environment (recommended)

python -m venv venv
venv\Scripts\activate   # (Windows)
source venv/bin/activate  # (Mac/Linux)


Install dependencies

pip install -r requirements.txt


or if you don’t have it yet, create one:

pip install streamlit PyPDF2 requests


Set your Groq API key

Either directly in the Streamlit sidebar

Or securely via a .streamlit/secrets.toml file:

[general]
GROQ_API_KEY = "your_api_key_here"

▶️ Run the App
streamlit run app.py


Then open the local URL (usually http://localhost:8501) in your browser.

🧠 How It Works

Upload a PDF

The app extracts its text using PyPDF2

Enter a question

The text + your query are sent to Groq’s LLM API

The model generates a context-aware answer

View chat history in the app interface

🧩 Example Models

mixtral-8x7b-32768

llama-3.1-8b-instant

gemma-7b-it

llama-3.3-70b-versatile