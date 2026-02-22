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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

graph = build_graph()


@app.get("/")
def health():
    return {"status": "Backend Running"}


@app.post("/upload")
async def upload_documents(files: List[UploadFile] = File(...)):

    all_docs = []
    os.makedirs("temp_docs", exist_ok=True)

    for file in files:
        path = os.path.join("temp_docs", file.filename)

        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        docs = load_and_split(path)
        all_docs.extend(docs)

    create_vectorstore(all_docs)

    return {"message": "Documents processed successfully"}


@app.post("/generate")
async def generate_quiz(
    single_n: int = Form(...),
    multi_n: int = Form(...),
    tf_n: int = Form(...),
    yn_n: int = Form(...),
    model: str = Form(...),
):

    if not os.path.exists("faiss_index"):
        return {"error": "Please upload documents first."}

    vectorstore = load_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    docs = retriever.invoke("Generate quiz")
    context = "\n\n".join([d.page_content for d in docs])

    result = graph.invoke({
        "context": context,
        "single_n": single_n,
        "multi_n": multi_n,
        "tf_n": tf_n,
        "yn_n": yn_n,
        "model": model,
    })

    questions = []
    base_id = int(time.time() * 1000)

    # SINGLE
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
                "type": "multi",
                "options": options,
                "correctAnswer": correct,
                "explanation": q.get("explanation", "")
            })

    # TRUE/FALSE
    for q in result.get("tf_output", []):
        questions.append({
            "id": base_id + random.randint(1, 99999),
            "text": q["question"],
            "type": "truefalse",
            "options": ["True", "False"],
            "correctAnswer": q["correct_answer"],
            "explanation": q.get("explanation", "")
        })

    # YES/NO
    for q in result.get("yn_output", []):
        questions.append({
            "id": base_id + random.randint(1, 99999),
            "text": q["question"],
            "type": "yesno",
            "options": ["Yes", "No"],
            "correctAnswer": q["correct_answer"],
            "explanation": q.get("explanation", "")
        })

    # DELETE VECTORSTORE
    reset_vectorstore()

    return {"questions": questions}