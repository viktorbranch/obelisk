"""Interface gráfica para conversar com Ollama e executar ações no navegador.

Uso:
    python examples/ollama_chat_interface.py

Requisitos:
    - Ollama rodando localmente
    - Navegador Chrome instalado
"""

import os
import sys
import json
import threading
import webbrowser
import time
from datetime import datetime
from typing import Optional, Dict, List

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
import requests

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print("Aviso: Selenium não instalado. Funcionalidades de automação limitadas.")

# Configurações do Ollama
BASE_URL = os.environ.get('OLLAMA_URL', 'http://127.0.0.1:11434')
MODEL = os.environ.get('OLLAMA_MODEL', 'llama3.2:latest')


class OllamaChat:
    """Cliente para comunicação com Ollama"""
    
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url
        self.model = model
        self.conversation_history = []
        
    def reset(self):
        """Limpa o histórico da conversa"""
        self.conversation_history = []
        
    def send_message(self, message: str) -> str:
        """Envia mensagem para o Ollama e retorna a resposta"""
        self.conversation_history.append({
            "role": "user",
            "content": message
        })
        
        try:
            response = requests.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": self.conversation_history,
                    "stream": False
                },
                timeout=120
            )
            response.raise_for_status()
            
            result = response.json()
            assistant_message = result['message']['content']
            
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message
            
        except requests.exceptions.ConnectionError:
            return "❌ Erro: Não foi possível conectar ao Ollama. Verifique se está rodando."
        except requests.exceptions.Timeout:
            return "❌ Erro: Timeout na conexão com o Ollama."
        except Exception as e:
            return f"❌ Erro: {str(e)}"


class BrowserController:
    """Controlador para abrir URLs no navegador"""
    
    @staticmethod
    def open_url(url: str) -> bool:
        """Abre URL no navegador padrão"""
        try:
            # Garante que a URL tem protocolo
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            webbrowser.open(url)
            return True
        except Exception as e:
            print(f"Erro ao abrir navegador: {e}")
            return False
    
    @staticmethod
    def search_google(query: str) -> bool:
        """Realiza busca no Google"""
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        return BrowserController.open_url(search_url)


class ChatInterface:
    """Interface gráfica para chat com Ollama"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Obelisk - Chat com Ollama")
        self.root.geometry("900x700")
        
        # Inicializa componentes
        self.ollama = OllamaChat(BASE_URL, MODEL)
        self.browser = BrowserController()
        
        # Configurar estilo
        self.setup_styles()
        
        # Criar interface
        self.create_widgets()
        
        # Verificar conexão com Ollama
        self.check_ollama_connection()
        
    def setup_styles(self):
        """Configura estilos da interface"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Cores
        self.bg_color = "#1e1e1e"
        self.fg_color = "#ffffff"
        self.input_bg = "#2d2d2d"
        self.button_bg = "#0e639c"
        self.assistant_bg = "#2d2d2d"
        self.user_bg = "#0e639c"
        
    def create_widgets(self):
        """Cria os widgets da interface"""
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header_frame = tk.Frame(main_frame, bg=self.bg_color)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = tk.Label(
            header_frame,
            text="🤖 Obelisk Chat",
            font=("Segoe UI", 18, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        )
        title_label.pack(side=tk.LEFT)
        
        self.status_label = tk.Label(
            header_frame,
            text="● Conectando...",
            font=("Segoe UI", 10),
            bg=self.bg_color,
            fg="#ffa500"
        )
        self.status_label.pack(side=tk.RIGHT)
        
        # Área de chat
        chat_frame = tk.Frame(main_frame, bg=self.bg_color)
        chat_frame.pack(fill=tk.BOTH, expand=True)
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            font=("Segoe UI", 10),
            bg=self.input_bg,
            fg=self.fg_color,
            insertbackground=self.fg_color,
            state=tk.DISABLED,
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        
        # Configurar tags para formatação
        self.chat_display.tag_config("user", foreground="#60a5fa", font=("Segoe UI", 10, "bold"))
        self.chat_display.tag_config("assistant", foreground="#34d399", font=("Segoe UI", 10, "bold"))
        self.chat_display.tag_config("system", foreground="#fbbf24", font=("Segoe UI", 9, "italic"))
        self.chat_display.tag_config("timestamp", foreground="#6b7280", font=("Segoe UI", 8))
        
        # Frame de entrada
        input_frame = tk.Frame(main_frame, bg=self.bg_color)
        input_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Campo de texto
        self.message_entry = tk.Text(
            input_frame,
            height=3,
            font=("Segoe UI", 10),
            bg=self.input_bg,
            fg=self.fg_color,
            insertbackground=self.fg_color,
            relief=tk.FLAT,
            padx=10,
            pady=10,
            wrap=tk.WORD
        )
        self.message_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        self.message_entry.bind("<Return>", self.on_enter_pressed)
        self.message_entry.bind("<Shift-Return>", lambda e: None)
        
        # Botões
        button_frame = tk.Frame(input_frame, bg=self.bg_color)
        button_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.send_button = tk.Button(
            button_frame,
            text="Enviar",
            command=self.send_message,
            bg=self.button_bg,
            fg=self.fg_color,
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.send_button.pack(fill=tk.X, pady=(0, 5))
        
        clear_button = tk.Button(
            button_frame,
            text="Limpar",
            command=self.clear_chat,
            bg="#374151",
            fg=self.fg_color,
            font=("Segoe UI", 9),
            relief=tk.FLAT,
            padx=20,
            pady=5,
            cursor="hand2"
        )
        clear_button.pack(fill=tk.X)
        
        # Mensagem de boas-vindas
        self.show_welcome_message()
        
    def show_welcome_message(self):
        """Mostra mensagem de boas-vindas"""
        welcome = """Bem-vindo ao Obelisk Chat! 🚀

Este assistente pode:
• Conversar e responder perguntas
• Abrir páginas web no navegador
• Realizar buscas no Google
• Executar comandos do sistema

Comandos especiais:
• /browser <url> - Abre uma URL no navegador
• /search <query> - Busca no Google
• /clear - Limpa o chat
• /reset - Reinicia a conversa

Digite sua mensagem e pressione Enter para começar!
"""
        self.add_message("Sistema", welcome, "system")
        
    def check_ollama_connection(self):
        """Verifica se o Ollama está acessível"""
        def check():
            try:
                response = requests.get(f"{BASE_URL}/api/tags", timeout=5)
                if response.status_code == 200:
                    self.update_status("● Conectado", "#34d399")
                else:
                    self.update_status("● Erro de conexão", "#ef4444")
            except:
                self.update_status("● Desconectado", "#ef4444")
                
        threading.Thread(target=check, daemon=True).start()
        
    def update_status(self, text: str, color: str):
        """Atualiza o status da conexão"""
        self.status_label.config(text=text, fg=color)
        
    def add_message(self, sender: str, message: str, tag: str = "user"):
        """Adiciona mensagem ao chat"""
        self.chat_display.config(state=tk.NORMAL)
        
        timestamp = datetime.now().strftime("%H:%M")
        
        if self.chat_display.get("1.0", tk.END).strip():
            self.chat_display.insert(tk.END, "\n\n")
            
        self.chat_display.insert(tk.END, f"[{timestamp}] ", "timestamp")
        self.chat_display.insert(tk.END, f"{sender}:\n", tag)
        self.chat_display.insert(tk.END, message)
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        
    def process_command(self, message: str) -> Optional[str]:
        """Processa comandos especiais"""
        message = message.strip()
        
        if message.startswith('/browser '):
            url = message[9:].strip()
            if self.browser.open_url(url):
                return f"✓ Navegador aberto: {url}"
            else:
                return f"✗ Erro ao abrir: {url}"
                
        elif message.startswith('/search '):
            query = message[8:].strip()
            if self.browser.search_google(query):
                return f"✓ Buscando no Google: {query}"
            else:
                return f"✗ Erro na busca: {query}"
                
        elif message == '/clear':
            self.clear_chat()
            return None
            
        elif message == '/reset':
            self.ollama.reset()
            return "✓ Conversa reiniciada"
            
        return None
        
    def check_for_browser_intent(self, user_message: str, response: str):
        """Verifica se a resposta indica necessidade de abrir navegador"""
        # Palavras-chave que indicam intenção de abrir navegador
        browser_keywords = [
            "vou abrir", "abrindo", "navegador", 
            "acesse", "visite", "abra o site",
            "vou buscar no google", "buscar no google"
        ]
        
        # Verifica se há URL na resposta
        import re
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', response)
        
        lower_response = response.lower()
        lower_message = user_message.lower()
        
        # Se menciona abrir navegador ou buscar
        if any(keyword in lower_response for keyword in browser_keywords):
            # Tenta extrair URL
            if urls:
                self.browser.open_url(urls[0])
                self.add_message("Sistema", f"✓ Navegador aberto: {urls[0]}", "system")
            # Se menciona busca no Google
            elif "google" in lower_response or "buscar" in lower_message:
                # Extrai termo de busca (simplificado)
                query = user_message.replace("busca", "").replace("buscar", "").replace("procure", "").strip()
                if query:
                    self.browser.search_google(query)
                    self.add_message("Sistema", f"✓ Busca realizada: {query}", "system")
        
    def send_message(self):
        """Envia mensagem para o Ollama"""
        message = self.message_entry.get("1.0", tk.END).strip()
        
        if not message:
            return
            
        # Limpa o campo de entrada
        self.message_entry.delete("1.0", tk.END)
        
        # Adiciona mensagem do usuário
        self.add_message("Você", message, "user")
        
        # Processa comandos especiais
        command_result = self.process_command(message)
        if command_result:
            self.add_message("Sistema", command_result, "system")
            if message == '/clear' or not command_result:
                return
        
        # Se não for comando, envia para Ollama
        if not message.startswith('/'):
            # Desabilita botão durante processamento
            self.send_button.config(state=tk.DISABLED, text="Pensando...")
            
            def get_response():
                response = self.ollama.send_message(message)
                
                # Adiciona resposta
                self.add_message("Assistente", response, "assistant")
                
                # Verifica se deve abrir navegador
                self.check_for_browser_intent(message, response)
                
                # Reabilita botão
                self.send_button.config(state=tk.NORMAL, text="Enviar")
                
            # Executa em thread separada
            threading.Thread(target=get_response, daemon=True).start()
            
    def on_enter_pressed(self, event):
        """Handler para tecla Enter"""
        if event.state & 0x1:  # Shift pressionado
            return None
        else:
            self.send_message()
            return "break"
            
    def clear_chat(self):
        """Limpa o chat"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete("1.0", tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self.show_welcome_message()


def main():
    """Função principal"""
    print(f"Iniciando Obelisk Chat Interface...")
    print(f"Ollama URL: {BASE_URL}")
    print(f"Modelo: {MODEL}")
    
    root = tk.Tk()
    app = ChatInterface(root)
    root.mainloop()


if __name__ == "__main__":
    main()
