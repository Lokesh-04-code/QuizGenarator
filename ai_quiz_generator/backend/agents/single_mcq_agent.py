import json
import re
from llm_factory import get_llm


def extract_json(text):
    match = re.search(r"\[.*\]", text, re.DOTALL)
    if match:
        return json.loads(match.group())
    return []


def generate_single_mcq(context, n, model):
    llm = get_llm(model)

    prompt = f"""
Generate {n} single correct MCQs.

STRICT RULES:
- EXACTLY 4 options.
- ONLY ONE correct answer.
- correct_answer MUST match one option EXACTLY.
- Return ONLY JSON.

FORMAT:
[
  {{
    "question": "",
    "options": ["A","B","C","D"],
    "correct_answer": "",
    "explanation": ""
  }}
]

Context:
{context}
"""

    response = llm.invoke(prompt).content.strip()
    return extract_json(response)