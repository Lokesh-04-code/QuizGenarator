import requests
import json

print('=== Testing Unified Endpoint ===')
url = 'http://localhost:8000/api/quizzes/generate-from-file'

# Open file
files = [
    ('documents', ('test_sample.txt', open('test_sample.txt', 'rb'), 'text/plain'))
]

# Send data exactly like frontend FormData
data = {
    'numMCQ': 1,
    'numMultiple': 1,
    'numTrueFalse': 1,
    'numYesNo': 1,
    'numQuestions': 4 # total
}

r = requests.post(url, files=files, data=data)

print('Status code:', r.status_code)

try:
    resp = r.json()
    if isinstance(resp, list):
        print(f"Success! Returned a list of {len(resp)} questions.")
        for i, q in enumerate(resp):
            print(f"\nQuestion {i+1} [{q.get('type')}]:")
            print(f"Text: {q.get('text')}")
            print(f"Options: {q.get('options')}")
            print(f"Answer: {q.get('correctAnswer')}")
    else:
        print("Response returned an object (error format?):", json.dumps(resp, indent=2))
except Exception as e:
    print("Failed to parse JSON response:", e)
    print("Raw response:", r.text)
