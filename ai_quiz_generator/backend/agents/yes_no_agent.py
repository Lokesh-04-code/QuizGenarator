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
Generate {n} Yes/No questions.

STRICT RULES:
- Correct answer MUST be exactly "Yes" or "No".
- Return ONLY JSON.

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