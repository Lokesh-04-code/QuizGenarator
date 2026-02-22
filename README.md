# 🧠 AI Quiz Generator

An AI-powered Quiz Generation System built using FastAPI, LangGraph, Groq LLM, Gemini Embeddings, FAISS, and Streamlit.

---

## 🚀 Features

- 📂 Upload PDF, DOCX, PPTX, TXT documents
- 🤖 AI-powered quiz generation using LLM
- 🧩 Supports:
  - Single Correct MCQ (4 options)
  - Multi Select MCQ (4 options, 1 or more correct)
  - True / False
  - Yes / No
- 🧠 Automatic correct answer mapping
- 📘 Explanation generation for every question
- 🗑 Automatic vector database deletion after quiz generation
- 📦 JSON formatted output

---

## 🐍 Python Version

```
Python 3.11.4
```

---

## 📦 Installation

Install all dependencies:

```bash
pip install -r requirements.txt
```

### ⚠ Important (for document processing support)

To ensure full document parsing capability, install:

```bash
pip install "unstructured[all-docs]"
```

This enables support for advanced PDF, DOCX, PPTX, and other file types.

---

## 📚 Core Libraries Used

```
fastapi==0.128.0
uvicorn==0.40.0
langchain==1.2.4
langchain-core==1.2.7
langchain-community==0.4.1
langchain-groq==1.1.1
langchain-google-genai==4.2.0
langchain-text-splitters==1.1.0
langgraph==1.0.6
groq==0.37.1
google-generativeai==0.8.6
faiss-cpu==1.13.2
pypdf==6.7.1
python-docx==1.2.0
python-pptx==1.0.2
unstructured==0.20.8
python-dotenv==1.2.1
python-multipart==0.0.21
requests==2.32.5
streamlit==1.53.0
pydantic==2.12.5
```

---


---

## ▶️ Backend Execution

Navigate to backend folder:

```bash
cd backend
```

Run the FastAPI server:

```bash
python -m uvicorn main:app --reload
```

Backend runs at:

```
http://127.0.0.1:8000
```

Swagger API docs:

```
http://127.0.0.1:8000/docs
```

---

## ▶️ Frontend Execution

Navigate to frontend folder:

```bash
cd frontend
```

Run the Streamlit application:

```bash
python -m streamlit run streamlit_app.py
```

Frontend runs at:

```
http://localhost:8501
```

---

## 📌 API Endpoints

- `POST /upload` → Upload documents and create vector database  
- `POST /generate` → Generate quiz questions  
- `GET /` → Health check  

---

## 📄 Output JSON Format

```json
{
  "questions": [
    {
      "id": 1771693842210,
      "text": "Question text here",
      "type": "single",
      "options": [
        "Option A",
        "Option B",
        "Option C",
        "Option D"
      ],
      "correctAnswer": "Option B",
      "explanation": "Detailed explanation here"
    }
  ]
}
```

For Multi-Select:

```json
{
  "type": "multi",
  "correctAnswer": [
    "Option A",
    "Option C"
  ]
}
```

---

## 🧠 Workflow

1. Upload documents  
2. Text is split and embedded using Gemini Embeddings  
3. FAISS vector database is created  
4. Relevant context retrieved  
5. LangGraph agents generate questions  
6. Output formatted into JSON  
7. Vector database automatically deleted  

---

## 🔐 Environment Variables

Create a `.env` file inside backend folder:

```
GROQ_API_KEY=your_groq_api_key
GEMINI_API_KEY=your_gemini_api_key
```

---

