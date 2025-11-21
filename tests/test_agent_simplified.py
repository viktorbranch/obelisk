"""
Teste Agent S3 SIMPLIFICADO - sem visão multimodal
Usa Ollama apenas para planejamento de texto, OCR local para grounding
"""
import os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import pyautogui
import time
import subprocess
from gui_agents.s3.core.mllm import LMMAgent

# Configuração
engine_params = {
    "engine_type": "llhama",
    "base_url": "http://127.0.0.1:11434",
    "model": "llama3.2:latest",
}

print("Inicializando LLM para planejamento...")
planner = LMMAgent(engine_params=engine_params)

# Instrução
task = "Abra o navegador Google Chrome e digite 'Funcionando...' na barra de busca"
print(f"\nTarefa: {task}\n")

# Usar LLM para gerar plano de ações
planner.reset()
planner.add_message(
    f"""Você é um assistente que cria planos de ação step-by-step para controlar um computador.
    
Tarefa: {task}

Gere um plano de ações simples, uma ação por linha, usando comandos Python/pyautogui.
Exemplo de formato:
1. subprocess.Popen(['chrome.exe'])
2. time.sleep(2)
3. pyautogui.hotkey('ctrl', 'l')
4. pyautogui.write('texto')
5. pyautogui.press('enter')

Retorne APENAS o plano numerado, sem explicações.""",
    role='user'
)

print("Gerando plano com LLM...")
response = planner.get_response()
print(f"\nPlano gerado:\n{response}\n")

# Extrair comandos do plano
import re
commands = []
for line in response.split('\n'):
    # Procurar por linhas que contenham comandos Python
    if any(keyword in line for keyword in ['subprocess', 'pyautogui', 'time.sleep']):
        # Extrair o comando após o número
        match = re.search(r'\d+\.\s*(.*)', line)
        if match:
            commands.append(match.group(1).strip())

if not commands:
    print("Não foi possível extrair comandos do plano. Usando plano fixo...")
    commands = [
        "subprocess.Popen(['C:\\\\Program Files\\\\Google\\\\Chrome\\\\Application\\\\chrome.exe'])",
        "time.sleep(3)",
        "pyautogui.hotkey('ctrl', 'l')",
        "time.sleep(1)",
        "pyautogui.write('Funcionando...', interval=0.1)",
        "pyautogui.press('enter')",
    ]

print(f"\nExecutando {len(commands)} comandos:\n")
for i, cmd in enumerate(commands, 1):
    print(f"Step {i}: {cmd}")
    # Corrigir caminho do Chrome se necessário
    if "chrome.exe" in cmd and "Program Files" not in cmd:
        cmd = cmd.replace("chrome.exe", "C:\\\\Program Files\\\\Google\\\\Chrome\\\\Application\\\\chrome.exe")
        print(f"  (corrigido para: {cmd})")
    
    try:
        exec(cmd)
        time.sleep(0.5)
    except Exception as e:
        print(f"  Erro: {e}")

print("\n=== Teste concluído! ===")
