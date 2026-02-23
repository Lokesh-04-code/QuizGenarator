import requests
import json

print('=== STEP 1: Upload ===')
with open('test_sample.txt', 'rb') as f:
    r = requests.post('http://localhost:8000/upload', files={'files': ('test_sample.txt', f, 'text/plain')})
print('Status:', r.status_code)
print('Response:', r.json())

print('\n=== STEP 2: Generate Quiz ===')
data = {
    'single_n': 2,
    'multi_n': 1,
    'tf_n': 1,
    'yn_n': 1,
    'model': 'llama-3.3-70b-versatile'
}
r2 = requests.post('http://localhost:8000/generate', data=data)
print('Status:', r2.status_code)

resp = r2.json()
if 'error' in resp:
    print('ERROR:', resp['error'])
elif 'questions' in resp:
    print('Total questions generated:', len(resp['questions']))
    for q in resp['questions']:
        print('[' + q['type'].upper() + '] ' + q['text'])
        print('    Options:', q['options'])
        print('    Answer:', q['correctAnswer'])
        print()
else:
    print('Unexpected response:', json.dumps(resp, indent=2))
