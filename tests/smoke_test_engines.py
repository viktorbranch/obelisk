import sys, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

variants = ['s2', 's2_5', 's3']
python = sys.executable or 'python'
wrapper = os.path.join(ROOT, 'scripts', 'llhama_wrapper.py')

for v in variants:
    print('\n--- Testing variant', v)
    try:
        module = __import__(f'gui_agents.{v}.core.mllm', fromlist=['LMMAgent'])
        LMMAgent = module.LMMAgent
    except Exception as e:
        print('Import error:', e)
        continue

    # Test local wrapper
    try:
        engine_params = {
            'engine_type': 'llhama',
            'model': 'llhama-mock',
            'local': True,
            'local_cmd': f'{python} "{wrapper}"',
        }
        agent = LMMAgent(engine_params=engine_params)
        agent.reset()
        agent.add_message('Teste local mock', role='user')
        resp = agent.get_response()
        print('Local mock response:', resp)
    except Exception as e:
        print('Local mock failed:', e)

    # Test Ollama if available
    try:
        base_url = 'http://127.0.0.1:11434'
        engine_params = {
            'engine_type': 'llhama',
            'base_url': base_url,
            'model': 'llama3.2:latest',
        }
        agent = LMMAgent(engine_params=engine_params)
        agent.reset()
        agent.add_message('Diga olá', role='user')
        resp = agent.get_response()
        print('Ollama response:', resp)
    except Exception as e:
        print('Ollama test failed (may be OK if Ollama not running):', e)
