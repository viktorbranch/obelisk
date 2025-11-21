"""Exemplo: roda um pequeno teste do LMMAgent apontando para Ollama local.

Uso:
    python examples/ollama_run.py

Altere `BASE_URL` e `MODEL` conforme necessário.
"""

import os
import sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from gui_agents.s3.core.mllm import LMMAgent

BASE_URL = os.environ.get('OLLAMA_URL', 'http://127.0.0.1:11434')
MODEL = os.environ.get('OLLAMA_MODEL', 'llama3.2:latest')

engine_params = {
    'engine_type': 'llhama',
    'base_url': BASE_URL,
    'model': MODEL,
}

print(f'Using Ollama at {BASE_URL} model {MODEL}')
agent = LMMAgent(engine_params=engine_params)
agent.reset()
agent.add_message('Diga olá em português', role='user')
resp = agent.get_response()
print('\n=== Response ===')
print(resp)
print('===============')
