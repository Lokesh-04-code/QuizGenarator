from langchain_groq import ChatGroq
from config import GROQ_API_KEY


def get_llm(model_name: str):
    return ChatGroq(
        model=model_name,
        groq_api_key=GROQ_API_KEY,
        temperature=0.3
    )