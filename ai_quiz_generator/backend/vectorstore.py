import os
import shutil
from langchain_community.vectorstores import FAISS
from embeddings import get_embeddings
from config import FAISS_PATH


def create_vectorstore(docs):
    embeddings = get_embeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(FAISS_PATH)
    return vectorstore


def load_vectorstore():
    embeddings = get_embeddings()
    return FAISS.load_local(
        FAISS_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )


def reset_vectorstore():
    if os.path.exists(FAISS_PATH):
        shutil.rmtree(FAISS_PATH)