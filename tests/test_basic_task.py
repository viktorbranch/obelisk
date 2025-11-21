"""
Teste básico: Agent S3 com Ollama local abre Google e digita "Funcionando..."
"""
import os
import sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import pyautogui
import io
from gui_agents.s3.agents.agent_s import AgentS3
from gui_agents.s3.agents.grounding import OSWorldACI

# Configuração
current_platform = "windows"

# Engine params para Ollama
engine_params = {
    "engine_type": "llhama",
    "base_url": "http://127.0.0.1:11434",
    "model": "llama3.2:latest",
}

# Engine params para grounding (usar Ollama também, sem modelo externo)
engine_params_for_grounding = {
    "engine_type": "llhama",
    "base_url": "http://127.0.0.1:11434",
    "model": "llama3.2:latest",
    "grounding_width": 1920,
    "grounding_height": 1080,
}

# Inicializar grounding agent OSWorldACI
grounding_agent = OSWorldACI(
    env=None,  # No local env for basic test
    platform=current_platform,
    engine_params_for_generation=engine_params,
    engine_params_for_grounding=engine_params_for_grounding,
    width=1920,
    height=1080,
)

# Inicializar Agent S3
print("Inicializando Agent S3 com Ollama...")
agent = AgentS3(
    engine_params,
    grounding_agent,
    platform=current_platform,
    max_trajectory_length=8,
    enable_reflection=False  # Desabilitar reflection para teste simples
)

# Instrução
instruction = "Abra o navegador Google Chrome e digite 'Funcionando...' na barra de busca"

print(f"Instrução: {instruction}")
print("Executando...")

# Loop de execução (máximo 10 steps para teste)
max_steps = 10
for step in range(max_steps):
    print(f"\n--- Step {step + 1} ---")
    
    # Capturar screenshot
    screenshot = pyautogui.screenshot()
    buffered = io.BytesIO()
    screenshot.save(buffered, format="PNG")
    screenshot_bytes = buffered.getvalue()
    
    obs = {
        "screenshot": screenshot_bytes,
    }
    
    # Obter ação do agente
    try:
        info, action = agent.predict(instruction=instruction, observation=obs)
        print(f"Info: {info}")
        print(f"Action: {action}")
        
        # Executar ação
        if action and len(action) > 0:
            action_code = action[0]
            print(f"Executando: {action_code}")
            exec(action_code)
            
            # Verificar se terminou
            if "DONE" in str(info) or "done" in action_code.lower():
                print("\nTarefa concluída!")
                break
        else:
            print("Nenhuma ação retornada")
            break
            
    except Exception as e:
        print(f"Erro no step {step + 1}: {e}")
        import traceback
        traceback.print_exc()
        break
    
    # Pequeno delay entre ações
    import time
    time.sleep(2)

print("\n=== Teste finalizado ===")
