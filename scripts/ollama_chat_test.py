import json
import urllib.request

url = 'http://127.0.0.1:11434/v1/chat/completions'
with open('scripts/payload.json','r',encoding='utf-8') as f:
    data = f.read()
req = urllib.request.Request(url, data=data.encode('utf-8'), headers={'Content-Type': 'application/json'})
with urllib.request.urlopen(req, timeout=30) as resp:
    print(resp.read().decode('utf-8'))
