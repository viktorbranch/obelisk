import os, sys
# Ensure package import works when running as a script
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from gui_agents.s3.core.mllm import LMMAgent

engine_params = {
    'engine_type': 'llhama',
    'base_url': 'http://127.0.0.1:11434',
    'model': 'llama3.2:latest',
}

print('Instantiating LMMAgent with Ollama...')
agent = LMMAgent(engine_params=engine_params)
agent.reset()
agent.add_message('Diga olá em português', role='user')
resp = agent.get_response()
print('\n=== Response from Ollama via LMMAgent ===')
print(resp)
print('=======================================')
