import json
import re
from llm_factory import get_llm


def extract_json(text):
    match = re.search(r"\[.*\]", text, re.DOTALL)
    if match:
        return json.loads(match.group())
    return []


def generate_true_false(context, n, model):
    llm = get_llm(model)

    prompt = f"""
Generate EXACTLY {n} True/False questions. You MUST generate exactly {n} questions, no more, no less.

STRICT RULES:
- Generate EXACTLY {n} questions. Not {n-1}, not {n+1}. EXACTLY {n}.
- Correct answer MUST be exactly "True" or "False".
- Return ONLY a valid JSON array, no extra text or explanation outside JSON.

FORMAT:
[
  {{
    "question": "",
    "correct_answer": "True",
    "explanation": ""
  }}
]

Context:
{context}
"""

    response = llm.invoke(prompt).content.strip()
    return extract_json(response)