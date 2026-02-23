import json
import re
from llm_factory import get_llm


def extract_json(text):
    match = re.search(r"\[.*\]", text, re.DOTALL)
    if match:
        return json.loads(match.group())
    return []


def generate_yes_no(context, n, model):
    llm = get_llm(model)

    prompt = f"""
Generate EXACTLY {n} Yes/No questions. You MUST generate exactly {n} questions, no more, no less.

STRICT RULES:
- Generate EXACTLY {n} questions. Not {n-1}, not {n+1}. EXACTLY {n}.
- Correct answer MUST be exactly "Yes" or "No".
- Return ONLY a valid JSON array, no extra text or explanation outside JSON.

FORMAT:
[
  {{
    "question": "",
    "correct_answer": "Yes",
    "explanation": ""
  }}
]

Context:
{context}
"""

    response = llm.invoke(prompt).content.strip()
    return extract_json(response)