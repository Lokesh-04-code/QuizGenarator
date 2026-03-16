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
Generate EXACTLY {n} multi-select MCQs. You MUST generate exactly {n} questions, no more, no less.

STRICT RULES:
- Generate EXACTLY {n} questions. Not {n-1}, not {n+1}. EXACTLY {n}.
- EXACTLY 4 options per question.
- At least 1 correct answer, maximum 4 correct answers.
- correct_answers MUST match options EXACTLY (word for word).
- Provide options as pure text ONLY. Do NOT prefix options with letters or numbers (e.g., do NOT use 'A) ', 'B) ', '1. ', etc.). Just the exact option text itself.
- Return ONLY a valid JSON array, no extra text or explanation outside JSON.

FORMAT:
[
  {{
    "question": "",
    "options": ["Option text 1", "Option text 2", "Option text 3", "Option text 4"],
    "correct_answers": ["Option text 1", "Option text 3"],
    "explanation": ""
  }}
]

Context:
{context}
"""

    response = llm.invoke(prompt).content.strip()
    return extract_json(response)