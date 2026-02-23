from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os
import shutil
import time
import random

from document_loader import load_and_split
from vectorstore import create_vectorstore, load_vectorstore, reset_vectorstore
from graph.graph_builder import build_graph


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

graph = build_graph()

ALLOWED_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "gemma2-9b-it",
    "llama-3.2-3b-preview",
]
DEFAULT_MODEL = ALLOWED_MODELS[0]


@app.get("/")
def health():
    return {"status": "Backend Running"}


@app.get("/api/models")
def get_models():
    return {"models": ALLOWED_MODELS, "default": DEFAULT_MODEL}


@app.post("/api/quizzes/generate-from-file")
async def generate_from_file(
    documents: List[UploadFile] = File(...),
    numMCQ: int = Form(...),
    numMultiple: int = Form(...),
    numTrueFalse: int = Form(...),
    numYesNo: int = Form(...),
    numQuestions: int = Form(...),
    model: str = Form(DEFAULT_MODEL),
):
    try:
        all_docs = []
        os.makedirs("temp_docs", exist_ok=True)
        
        # 1. Process all uploaded documents
        for file in documents:
            path = os.path.join("temp_docs", file.filename)
            with open(path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            docs = load_and_split(path)
            all_docs.extend(docs)
            
        if not all_docs:
            return {"msg": "No valid text found in documents."}
            
        # Create temporary vectorstore for this request
        create_vectorstore(all_docs)
        vectorstore = load_vectorstore()
        retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
        
        # 2. Retrieve context and generate questions
        docs = retriever.invoke("Generate quiz")
        context = "\n\n".join([d.page_content for d in docs])
        
        # Validate model selection
        if model not in ALLOWED_MODELS:
            model = DEFAULT_MODEL
        
        result = graph.invoke({
            "context": context,
            "single_n": numMCQ,
            "multi_n": numMultiple,
            "tf_n": numTrueFalse,
            "yn_n": numYesNo,
            "model": model,
        })
        
        questions = []
        base_id = int(time.time() * 1000)
        
        # SINGLE (MCQ)
        for q in result.get("single_output", []):
            if len(q.get("options", [])) == 4:
                questions.append({
                    "id": base_id + random.randint(1, 99999),
                    "text": q["question"],
                    "type": "single",
                    "options": q["options"],
                    "correctAnswer": q["correct_answer"],
                    "explanation": q.get("explanation", "")
                })

        # MULTI
        for q in result.get("multi_output", []):
            options = q.get("options", [])
            correct = q.get("correct_answers", [])
            if len(options) == 4 and len(correct) >= 1:
                questions.append({
                    "id": base_id + random.randint(1, 99999),
                    "text": q["question"],
                    "type": "multiple",
                    "options": options,
                    "correctAnswer": correct,
                    "explanation": q.get("explanation", "")
                })

        # TRUE/FALSE
        for q in result.get("tf_output", []):
            questions.append({
                "id": base_id + random.randint(1, 99999),
                "text": q["question"],
                "type": "true-false",
                "options": ["True", "False"],
                "correctAnswer": q["correct_answer"],
                "explanation": q.get("explanation", "")
            })

        # YES/NO
        for q in result.get("yn_output", []):
            questions.append({
                "id": base_id + random.randint(1, 99999),
                "text": q["question"],
                "type": "yes-no"
                ,
                "options": ["Yes", "No"],
                "correctAnswer": q["correct_answer"],
                "explanation": q.get("explanation", "")
            })
            
        return questions

    except Exception as e:
        return {"msg": f"Failed to generate quiz: {str(e)}"}
        
    finally:
        # 3. Cleanup after generation
        try:
            reset_vectorstore()
            if os.path.exists("temp_docs"):
                shutil.rmtree("temp_docs")
        except Exception:
            pass

@app.post("/api/quizzes/generate-from-topic")
async def generate_from_topic(
    topic: str = Form(...),
    numMCQ: int = Form(...),
    numMultiple: int = Form(...),
    numTrueFalse: int = Form(...),
    numYesNo: int = Form(...),
    numQuestions: int = Form(...),
    model: str = Form(DEFAULT_MODEL),
):
    try:
        if not topic or not topic.strip():
            return {"msg": "Topic cannot be empty."}
            
        # Validate model selection
        if model not in ALLOWED_MODELS:
            model = DEFAULT_MODEL
        
        result = graph.invoke({
            "context": f"Detailed information about the topic: {topic}",
            "single_n": numMCQ,
            "multi_n": numMultiple,
            "tf_n": numTrueFalse,
            "yn_n": numYesNo,
            "model": model,
        })
        
        questions = []
        base_id = int(time.time() * 1000)
        
        # SINGLE (MCQ)
        for q in result.get("single_output", []):
            if len(q.get("options", [])) == 4:
                questions.append({
                    "id": base_id + random.randint(1, 99999),
                    "text": q["question"],
                    "type": "single",
                    "options": q["options"],
                    "correctAnswer": q["correct_answer"],
                    "explanation": q.get("explanation", "")
                })

        # MULTI
        for q in result.get("multi_output", []):
            options = q.get("options", [])
            correct = q.get("correct_answers", [])
            if len(options) == 4 and len(correct) >= 1:
                questions.append({
                    "id": base_id + random.randint(1, 99999),
                    "text": q["question"],
                    "type": "multiple",
                    "options": options,
                    "correctAnswer": correct,
                    "explanation": q.get("explanation", "")
                })

        # TRUE/FALSE
        for q in result.get("tf_output", []):
            questions.append({
                "id": base_id + random.randint(1, 99999),
                "text": q["question"],
                "type": "true-false",
                "options": ["True", "False"],
                "correctAnswer": q["correct_answer"],
                "explanation": q.get("explanation", "")
            })

        # YES/NO
        for q in result.get("yn_output", []):
            questions.append({
                "id": base_id + random.randint(1, 99999),
                "text": q["question"],
                "type": "yes-no",
                "options": ["Yes", "No"],
                "correctAnswer": q["correct_answer"],
                "explanation": q.get("explanation", "")
            })
            
        return questions

    except Exception as e:
        return {"msg": f"Failed to generate quiz: {str(e)}"}