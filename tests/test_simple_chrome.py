"""
Teste básico SIMPLIFICADO: Abre Chrome e digita texto usando pyautogui direto
Sem usar Agent S (para verificar se o ambiente funciona)
"""
import pyautogui
import time
import subprocess

print("=== Teste Básico Simplificado ===")
print("1. Abrindo Chrome...")

try:
    # Abrir Chrome via subprocess
    subprocess.Popen(['C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'])
    time.sleep(3)
    
    print("2. Aguardando Chrome abrir...")
    time.sleep(2)
    
    print("3. Clicando na barra de endereço (Ctrl+L)...")
    pyautogui.hotkey('ctrl', 'l')
    time.sleep(1)
    
    print("4. Digitando 'Funcionando...'")
    pyautogui.write('Funcionando...', interval=0.1)
    time.sleep(1)
    
    print("5. Pressionando Enter...")
    pyautogui.press('enter')
    
    print("\n=== Teste concluído com sucesso! ===")
    
except Exception as e:
    print(f"Erro: {e}")
    import traceback
    traceback.print_exc()
