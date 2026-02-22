import json
import re
from llm_factory import get_llm


def extract_json(text):
    match = re.search(r"\[.*\]", text, re.DOTALL)
    if match:
        return json.loads(match.group())
    return []


def generate_multi_mcq(context, n, model):
    llm = get_llm(model)

    prompt = f"""
Generate {n} multi-select MCQs.

STRICT RULES:
- EXACTLY 4 options.
- At least 1 correct answer.
- Maximum 4 correct answers.
- correct_answers MUST match options EXACTLY.
- Return ONLY JSON.

FORMAT:
[
  {{
    "question": "",
    "options": ["A","B","C","D"],
    "correct_answers": ["A","C"],
    "explanation": ""
  }}
]

Context:
{context}
"""

    response = llm.invoke(prompt).content.strip()
    return extract_json(response)