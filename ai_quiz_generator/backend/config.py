import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from current dir or parent dir (works locally)
# On Render, env vars are set via dashboard, so this is a no-op
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

EMBED_MODEL = "models/gemini-embedding-001"
FAISS_PATH = "faiss_index"