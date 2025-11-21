import json
import urllib.request

url = 'http://127.0.0.1:11434/v1/completions'
payload = {
    'model': 'llama3.2:latest',
    'prompt': 'Olá Ollama!',
    'max_tokens': 50,
}
req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
with urllib.request.urlopen(req, timeout=10) as resp:
    print(resp.read().decode('utf-8'))
