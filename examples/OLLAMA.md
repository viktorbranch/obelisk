# Usando Ollama (local) com Agent-S

Este guia descreve como usar o Ollama (daemon local) como backend LLM para o Agent-S.

Requisitos
- Ollama instalado e rodando localmente (padrão: `http://127.0.0.1:11434`).
- Modelo baixado no Ollama (ex.: `llama3.2:latest`).

Passos rápidos
1. Verifique o daemon:
```cmd
curl http://127.0.0.1:11434/
# Deve responder "Ollama is running"
```
2. Liste modelos instalados:
```cmd
curl http://127.0.0.1:11434/v1/models
```
3. Teste uma geração simples (OpenAI-style):
```cmd
curl -X POST "http://127.0.0.1:11434/v1/chat/completions" -H "Content-Type: application/json" -d "{\"model\":\"llama3.2:latest\",\"messages\":[{\"role\":\"user\",\"content\":\"Olá Ollama!\"}]}"
```

Usando no Agent-S via Python
- Exemplo rápido (veja `examples/ollama_run.py`):
```python
engine_params = {
  "engine_type": "llhama",
  "base_url": "http://127.0.0.1:11434",
  "model": "llama3.2:latest",
}
from gui_agents.s3.core.mllm import LMMAgent
agent = LMMAgent(engine_params=engine_params)
agent.reset()
agent.add_message('Diga olá em português', role='user')
resp = agent.get_response()
print(resp)
```

Usando o CLI `agent_s`
- O CLI aceita `--provider openai` com `--model_url` apontando para o endpoint Ollama:
```cmd
agent_s --provider openai --model llama3.2:latest --model_url http://127.0.0.1:11434 --ground_provider huggingface --ground_url http://localhost:8080 --ground_model ui-tars-1.5-7b --grounding_width 1920 --grounding_height 1080
```

Notas
- `engine_type: "llhama"` é a implementação custom que adicionamos para integrar com Ollama (modo HTTP) ou com wrappers locais (modo `local`).
- Se preferir rodar o LLM localmente sem Ollama, crie um wrapper que leia stdin e escreva a resposta em stdout e use `engine_params["local"] = True` e `engine_params["local_cmd"] = "python path\\to\\wrapper.py"`.
- Ajuste timeouts e `max_tokens` conforme necessário para modelos grandes.

Se quiser, eu posso gerar um `README` mais detalhado, ou um `requirements` example para integrar `ctransformers`/`transformers` localmente.
