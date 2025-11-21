import os
import sys
import time

# Ensure workspace package imports work
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from gui_agents.s3.core.mllm import LMMAgent

# Path to the wrapper script
wrapper = os.path.join(ROOT, 'scripts', 'llhama_wrapper.py')
python = sys.executable or 'python'

engine_params = {
    'engine_type': 'llhama',
    'model': 'llhama-mock',
    'local': True,
    'local_cmd': f'{python} "{wrapper}"',
}

print('Instantiating LMMAgent with local Llhama wrapper...')
agent = LMMAgent(engine_params=engine_params)

# Send a simple message and get response
agent.reset()
agent.add_message('Hello, please say hi back from Llhama mock', role='user')
print('Messages prepared. Calling get_response...')
resp = agent.get_response()
print('\n=== Response from Llhama (mock) ===')
print(resp)
print('===================================')
