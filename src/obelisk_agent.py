"""Obelisk AI - Autonomous Computer Agent

An intelligent autonomous agent that can see, think, and act on your computer.

Features:
    - Autonomous task execution with vision and planning
    - Web automation with Selenium and BeautifulSoup
    - Complete system control with PyAutoGUI
    - Natural language interface with Ollama
    - Real-time screen monitoring and analysis

Usage:
    python -m src.obelisk_agent
    # or
    python src/obelisk_agent.py

Requirements:
    - Python 3.8+
    - Ollama running locally (http://127.0.0.1:11434)
    - pip install -r requirements.txt

Author: Obelisk AI Team
License: MIT
Version: 1.0.0
"""

import os
import sys
import threading
import time
import subprocess
import pyautogui
import base64
import json
import re
from datetime import datetime
from typing import Optional, Dict, List
from io import BytesIO

import tkinter as tk
from tkinter import scrolledtext, ttk
import requests

# Import do processador de intenções
try:
    from src.core.intent_processor import IntentProcessor
    INTENT_PROCESSOR_AVAILABLE = True
except ImportError:
    try:
        from core.intent_processor import IntentProcessor
        INTENT_PROCESSOR_AVAILABLE = True
    except ImportError:
        INTENT_PROCESSOR_AVAILABLE = False
        print("⚠️  intent_processor.py não encontrado - usando modo básico")
except ImportError:
    INTENT_PROCESSOR_AVAILABLE = False
    print("⚠️  intent_processor.py não encontrado - usando modo básico")

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, NoSuchElementException, InvalidSessionIdException
    from bs4 import BeautifulSoup
    SELENIUM_AVAILABLE = True
    BS4_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    BS4_AVAILABLE = False
    print("⚠️  Instale as dependências: pip install selenium beautifulsoup4")

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
        
    def add_system_context(self, context: str):
        """Adiciona contexto do sistema à conversa"""
        self.conversation_history.append({
            "role": "system",
            "content": context
        })
    
    def send_message(self, message: str, context: str = None) -> str:
        """Envia mensagem para o Ollama e retorna a resposta"""
        
        # Adiciona instruções de comportamento proativo se tiver contexto web
        if context:
            enhanced_context = "INSTRUÇÕES DE COMPORTAMENTO:\n"
            enhanced_context += "- Você é um assistente PROATIVO que EXECUTA AÇÕES automaticamente\n"
            enhanced_context += "- Quando o usuário pedir algo (ex: 'pesquise X'), você JÁ FEZ a ação\n"
            enhanced_context += "- NÃO pergunte 'quer que eu faça?', apenas FAÇA e REPORTE o resultado\n"
            enhanced_context += "- Se precisar de mais passos, SUGIRA próximas ações específicas\n"
            enhanced_context += "- Seja direto, objetivo e mostre os RESULTADOS encontrados\n\n"
            enhanced_context += context
            self.add_system_context(enhanced_context)
        
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


class AutonomousAgent:
    """Agente autônomo que vê a tela, planeja e executa ações"""
    
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url
        self.model = model
        self.current_task = None
        self.task_steps = []
        self.completed_steps = []
        self.max_iterations = 20
        
    def capture_screen(self) -> str:
        """Captura a tela e converte para base64"""
        try:
            screenshot = pyautogui.screenshot()
            buffered = BytesIO()
            screenshot.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            return img_str
        except Exception as e:
            print(f"Erro ao capturar tela: {e}")
            return None
    
    def analyze_screen_with_vision(self, task: str, screen_b64: str) -> Dict:
        """Analisa a tela e determina próximos passos usando Ollama"""
        try:
            # Captura informações da tela sem visão
            screen_info = self.get_screen_info()
            
            # Monta prompt para análise
            prompt = f"""TAREFA DO USUÁRIO: {task}

INFORMAÇÕES DA TELA ATUAL:
- Posição do mouse: {screen_info['mouse_pos']}
- Tamanho da tela: {screen_info['screen_size']}
- Janela ativa: {screen_info.get('active_window', 'Desconhecido')}

INSTRUÇÕES:
Você é um agente autônomo executando uma tarefa.
Determine o próximo passo lógico para completar: "{task}"

Responda APENAS em formato JSON:
{{
    "observacao": "o que você deduz sobre a situação atual",
    "proximo_passo": "descrição clara do próximo passo",
    "acao": "SEARCH | OPEN_APP | TYPE | PRESS_KEY | WAIT | DONE",
    "parametros": {{"detalhe": "valor específico"}},
    "progresso": 0-100
}}

AÇÕES DISPONÍVEIS:
- SEARCH: Buscar no Google (parametros: {{"query": "termo"}})
- OPEN_APP: Abrir programa (parametros: {{"app": "nome"}})
- TYPE: Digitar texto (parametros: {{"texto": "conteúdo"}})
- PRESS_KEY: Pressionar tecla (parametros: {{"key": "enter/esc/tab"}})
- WAIT: Aguardar (parametros: {{"segundos": 2}})
- DONE: Tarefa completa

Seja OBJETIVO e PRAGMÁTICO. Escolha a ação mais direta.
"""
            
            # Envia para Ollama
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={{
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                }},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                response_text = result.get('response', '')
                
                # Tenta extrair JSON
                try:
                    json_match = re.search(r'\{{.*\}}', response_text, re.DOTALL)
                    if json_match:
                        data = json.loads(json_match.group(0))
                        return data
                except:
                    pass
                
                # Fallback: cria resposta padrão baseada na tarefa
                return self.create_default_action(task)
            
            return self.create_default_action(task)
            
        except Exception as e:
            print(f"Erro na análise: {{e}}")
            return self.create_default_action(task)
    
    def get_screen_info(self) -> Dict:
        """Obtém informações da tela sem usar visão"""
        try:
            mouse_x, mouse_y = pyautogui.position()
            screen_w, screen_h = pyautogui.size()
            
            return {{
                'mouse_pos': (mouse_x, mouse_y),
                'screen_size': (screen_w, screen_h),
                'timestamp': datetime.now().isoformat()
            }}
        except:
            return {{'mouse_pos': (0, 0), 'screen_size': (1920, 1080)}}
    
    def create_default_action(self, task: str) -> Dict:
        """Cria ação padrão baseada em palavras-chave da tarefa"""
        task_lower = task.lower()
        
        # Detecta intenção pela tarefa
        if any(word in task_lower for word in ['pesquise', 'busque', 'procure', 'google']):
            # Extrai termo de busca
            for word in ['pesquise', 'busque', 'procure']:
                if word in task_lower:
                    query = task_lower.split(word)[-1].strip()
                    query = re.sub(r'\s+(e|pela|pelo|por|sobre|a|o)\s+', ' ', query)
                    return {{
                        "observacao": f"Detectada necessidade de buscar: {{query}}",
                        "proximo_passo": f"Buscar '{{query}}' no Google",
                        "acao": "SEARCH",
                        "parametros": {{"query": query}},
                        "progresso": 20
                    }}
        
        if any(word in task_lower for word in ['abra', 'abre', 'execute']):
            # Detecta programa
            programs = {{
                'calculadora': 'calc',
                'bloco de notas': 'notepad',
                'notepad': 'notepad',
                'paint': 'mspaint',
                'explorador': 'explorer',
                'chrome': 'chrome',
                'firefox': 'firefox'
            }}
            
            for prog_name, prog_cmd in programs.items():
                if prog_name in task_lower:
                    return {{
                        "observacao": f"Detectada necessidade de abrir {{prog_name}}",
                        "proximo_passo": f"Abrir {{prog_name}}",
                        "acao": "OPEN_APP",
                        "parametros": {{"app": prog_cmd}},
                        "progresso": 50
                    }}
        
        # Ação padrão: aguardar
        return {{
            "observacao": "Analisando tarefa",
            "proximo_passo": "Aguardando análise completa",
            "acao": "WAIT",
            "parametros": {{"segundos": 1}},
            "progresso": 10
        }}
    
    def execute_action(self, action_data: Dict) -> bool:
        """Executa a ação determinada pela análise"""
        try:
            action = action_data.get('acao', '').upper()
            params = action_data.get('parametros', {})
            
            if action == "CLICK":
                # Clica em posição ou busca elemento
                if 'x' in params and 'y' in params:
                    pyautogui.click(params['x'], params['y'])
                elif 'texto' in params:
                    # Tenta encontrar texto na tela e clicar
                    location = pyautogui.locateOnScreen(params['texto'])
                    if location:
                        pyautogui.click(location)
                print(f"✓ Clique executado")
                return True
                
            elif action == "TYPE":
                # Digita texto
                text = params.get('texto', params.get('detalhe', ''))
                pyautogui.write(text, interval=0.05)
                print(f"✓ Digitado: {text[:50]}")
                return True
                
            elif action == "SEARCH":
                # Busca no Google
                query = params.get('query', params.get('detalhe', ''))
                # Abre Google e busca
                pyautogui.hotkey('win', 'r')
                time.sleep(0.5)
                pyautogui.write(f'https://www.google.com/search?q={query}')
                pyautogui.press('enter')
                print(f"✓ Busca iniciada: {query}")
                return True
                
            elif action == "OPEN_APP":
                # Abre aplicativo
                app = params.get('app', params.get('detalhe', ''))
                pyautogui.hotkey('win', 'r')
                time.sleep(0.5)
                pyautogui.write(app)
                pyautogui.press('enter')
                print(f"✓ Aplicativo aberto: {app}")
                return True
                
            elif action == "PRESS_KEY":
                # Pressiona tecla
                key = params.get('key', params.get('detalhe', ''))
                pyautogui.press(key)
                print(f"✓ Tecla pressionada: {key}")
                return True
                
            elif action == "WAIT":
                # Aguarda
                duration = params.get('segundos', 2)
                time.sleep(duration)
                print(f"✓ Aguardando {duration}s")
                return True
                
            elif action == "DONE":
                print("✓ Tarefa concluída!")
                return True
                
            return False
            
        except Exception as e:
            print(f"✗ Erro ao executar ação: {e}")
            return False
    
    def run_autonomous_task(self, task: str, progress_callback=None) -> List[str]:
        """Executa tarefa de forma autônoma com loop de visão-análise-ação"""
        self.current_task = task
        self.task_steps = []
        self.completed_steps = []
        
        iteration = 0
        
        while iteration < self.max_iterations:
            iteration += 1
            
            # 1. Captura a tela
            if progress_callback:
                progress_callback(f"🔍 Iteração {iteration}: Capturando tela...")
            
            screen = self.capture_screen()
            if not screen:
                break
            
            # 2. Analisa com visão
            if progress_callback:
                progress_callback(f"🧠 Analisando situação atual...")
            
            analysis = self.analyze_screen_with_vision(task, screen)
            if not analysis:
                break
            
            # 3. Registra observação
            step_desc = f"[{iteration}] {analysis.get('observacao', 'N/A')}"
            self.task_steps.append(step_desc)
            
            if progress_callback:
                progress_callback(f"📊 Progresso: {analysis.get('progresso', 0)}%")
                progress_callback(f"👁️ Vejo: {analysis.get('observacao', '')[:100]}")
                progress_callback(f"▶️ Próximo passo: {analysis.get('proximo_passo', '')}")
            
            # 4. Verifica se terminou
            if analysis.get('acao') == 'DONE':
                self.completed_steps.append("Tarefa concluída!")
                if progress_callback:
                    progress_callback("✅ TAREFA COMPLETA!")
                break
            
            # 5. Executa a ação
            if progress_callback:
                progress_callback(f"⚡ Executando: {analysis.get('acao')}")
            
            success = self.execute_action(analysis)
            
            if success:
                self.completed_steps.append(analysis.get('proximo_passo', 'Ação executada'))
            
            # 6. Aguarda antes da próxima iteração
            time.sleep(2)
        
        return self.completed_steps


class BrowserController:
    """Controlador para abrir URLs e extrair conteúdo do navegador"""
    
    def __init__(self):
        self.driver = None
        self.selenium_enabled = SELENIUM_AVAILABLE
        
    def initialize_driver(self):
        """Inicializa o driver do Selenium com opções anti-detecção"""
        if not self.selenium_enabled:
            return False
            
        try:
            chrome_options = Options()
            
            # ANTI-DETECÇÃO: Remove flags de automação
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # ANTI-DETECÇÃO: User-Agent real (parece navegador normal)
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            
            # ANTI-DETECÇÃO: Desabilita recursos que denunciam bot
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            
            # PERFORMANCE: Desabilita recursos desnecessários
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            
            # PRIVACIDADE: Desabilita logging
            chrome_options.add_argument('--disable-logging')
            chrome_options.add_argument('--log-level=3')
            
            # OPCIONAL: Modo headless (sem janela visível) - descomentado para ver
            # chrome_options.add_argument('--headless=new')
            
            self.driver = webdriver.Chrome(options=chrome_options)
            
            # ANTI-DETECÇÃO: Remove webdriver property
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            })
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("✓ Driver do Chrome inicializado (modo stealth)")
            
            # Maximiza a janela para melhor visualização
            self.driver.maximize_window()
            
            return True
        except Exception as e:
            print(f"✗ Erro ao inicializar driver: {e}")
            print("  Certifique-se de ter o Chrome instalado")
            self.selenium_enabled = False
            return False
    
    def open_url(self, url: str) -> bool:
        """Abre URL no navegador com comportamento humano"""
        if not self.driver:
            return False
            
        try:
            # Garante que a URL tem protocolo
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
                
            self.driver.get(url)
            
            # ANTI-DETECÇÃO: Delay aleatório (simula leitura humana)
            import random
            time.sleep(random.uniform(1.5, 3.0))
            
            return True
        except Exception as e:
            print(f"Erro ao abrir URL: {e}")
            return False
    
    def search_google(self, query: str) -> bool:
        """Realiza busca no Google com comportamento anti-bot"""
        try:
            # ALTERNATIVA 1: Usar DuckDuckGo (sem reCAPTCHA)
            search_url = f"https://duckduckgo.com/?q={query.replace(' ', '+')}"
            
            # ALTERNATIVA 2: Google com parâmetros específicos
            # search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}&hl=pt-BR"
            
            success = self.open_url(search_url)
            
            # Verifica se caiu em reCAPTCHA
            if success and self.driver:
                try:
                    page_text = self.driver.page_source.lower()
                    if 'recaptcha' in page_text or 'captcha' in page_text:
                        print("⚠️  reCAPTCHA detectado! Usando DuckDuckGo como alternativa...")
                        # Força usar DuckDuckGo
                        search_url = f"https://duckduckgo.com/?q={query.replace(' ', '+')}"
                        return self.open_url(search_url)
                except:
                    pass
            
            return success
        except Exception as e:
            print(f"Erro na busca: {e}")
            return False
    
    def check_and_handle_captcha(self) -> bool:
        """Verifica se há reCAPTCHA e tenta contornar"""
        if not self.driver:
            return False
        
        try:
            page_source = self.driver.page_source.lower()
            current_url = self.driver.current_url
            
            # Detecta reCAPTCHA
            if 'recaptcha' in page_source or 'captcha' in page_source or 'unusual traffic' in page_source:
                print("⚠️  reCAPTCHA/CAPTCHA detectado!")
                print("💡 Opções:")
                print("   1. Aguarde 10-30 segundos (Google pode liberar)")
                print("   2. Use DuckDuckGo como alternativa (sem CAPTCHA)")
                print("   3. Resolva manualmente se necessário")
                
                # Aguarda um pouco (às vezes o Google libera)
                time.sleep(3)
                
                return True  # Indica que há CAPTCHA
            
            return False  # Sem CAPTCHA
            
        except Exception as e:
            print(f"Erro ao verificar CAPTCHA: {e}")
            return False
    
    def get_page_content(self) -> Dict[str, any]:
        """Extrai conteúdo da página atual"""
        if not self.driver:
            return {"error": "Driver não inicializado"}
            
        try:
            content = {
                "url": self.driver.current_url,
                "title": self.driver.title,
                "text": "",
                "headlines": [],
                "links": [],
                "paragraphs": [],
                "images": [],
                "meta": {}
            }
            
            # Pega o HTML da página
            html = self.driver.page_source
            
            # Analisa com BeautifulSoup se disponível
            if BS4_AVAILABLE:
                soup = BeautifulSoup(html, 'html.parser')
                
                # Remove scripts e styles
                for script in soup(["script", "style", "nav", "footer", "header"]):
                    script.decompose()
                
                # Extrai meta tags
                content["meta"] = {
                    "description": soup.find("meta", {"name": "description"})["content"] if soup.find("meta", {"name": "description"}) else "",
                    "keywords": soup.find("meta", {"name": "keywords"})["content"] if soup.find("meta", {"name": "keywords"}) else "",
                    "author": soup.find("meta", {"name": "author"})["content"] if soup.find("meta", {"name": "author"}) else ""
                }
                
                # Extrai parágrafos
                paragraphs = soup.find_all('p')
                content["paragraphs"] = [p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 50][:10]
                
                # Extrai headlines (h1-h6)
                headlines = []
                for i in range(1, 7):
                    for h in soup.find_all(f'h{i}'):
                        text = h.get_text(strip=True)
                        if text and len(text) > 10:
                            headlines.append({"level": i, "text": text})
                content["headlines"] = headlines[:20]
                
                # Extrai links importantes
                links = []
                for a in soup.find_all('a', href=True):
                    text = a.get_text(strip=True)
                    href = a['href']
                    if text and len(text) > 5 and len(text) < 100:
                        links.append({"text": text, "url": href})
                content["links"] = links[:20]
                
                # Extrai imagens
                images = []
                for img in soup.find_all('img', src=True):
                    alt = img.get('alt', '')
                    src = img['src']
                    if alt or src:
                        images.append({"alt": alt, "src": src})
                content["images"] = images[:10]
                
                # Texto completo limpo
                text = soup.get_text(separator=' ', strip=True)
                content["text"] = ' '.join(text.split())[:3000]  # Limita a 3000 chars
                
            else:
                # Fallback sem BeautifulSoup
                try:
                    body = self.driver.find_element(By.TAG_NAME, "body")
                    content["text"] = body.text[:2000]
                except:
                    pass
                
            return content
            
        except Exception as e:
            return {"error": str(e)}
    
    def get_google_news_headlines(self) -> List[str]:
        """Extrai manchetes do Google Notícias"""
        if not self.driver:
            print("❌ Driver não inicializado")
            return []
            
        try:
            print(f"🌐 Abrindo Google Notícias...")
            
            # Maximiza a janela para o usuário ver
            try:
                self.driver.maximize_window()
            except:
                pass
            
            self.open_url("https://news.google.com")
            time.sleep(5)  # Aguarda carregamento completo
            
            print(f"📄 Página carregada: {self.driver.title}")
            print(f"🔗 URL atual: {self.driver.current_url}")
            
            headlines = []
            
            # Lista de textos genéricos para filtrar
            filter_keywords = [
                "principais notícias", "principais noticias", "opções para você",
                "opcoes para voce", "ciência e tecnologia", "ciencia e tecnologia",
                "mais", "ver", "seguir", "para você", "para voce",
                "esportes", "entretenimento", "brasil", "mundo",
                "negócios", "negocios", "saúde", "saude",
                "menu", "navegação", "navegacao", "categorias",
                "top stories", "recommended", "suggestions"
            ]
            
            # Estratégia: Buscar links de artigos com texto significativo
            print(f"🔍 Tentando extrair manchetes...")
            
            try:
                # Seletor mais específico para artigos
                article_links = self.driver.find_elements(By.CSS_SELECTOR, "article a")
                print(f"  Encontrados {len(article_links)} links em artigos")
                
                for link in article_links[:50]:
                    try:
                        text = link.text.strip()
                        
                        # Filtros de qualidade
                        if not text or len(text) < 20:  # Muito curto
                            continue
                        if len(text) > 200:  # Muito longo
                            continue
                        
                        # Remove textos genéricos
                        text_lower = text.lower()
                        if any(keyword in text_lower for keyword in filter_keywords):
                            continue
                        
                        # Remove se começar com símbolos
                        if text.startswith(("•", "...", "-", "→", "›")):
                            continue
                        
                        # Remove se terminar com "..."
                        if text.endswith(("...", "mais", "ver mais")):
                            continue
                        
                        # Deve ter pelo menos uma letra maiúscula (indica título)
                        if not any(c.isupper() for c in text):
                            continue
                        
                        # Deve ter palavras completas (não apenas números/símbolos)
                        words = text.split()
                        if len(words) < 3:  # Muito poucas palavras
                            continue
                        
                        headlines.append(text)
                        
                    except:
                        continue
                
                print(f"  ✓ {len(headlines)} manchetes encontradas em links de artigos")
                
            except Exception as e:
                print(f"  ✗ Erro ao buscar links: {e}")
            
            # Estratégia alternativa: h3 e h4 dentro de artigos
            if len(headlines) < 5:
                print("⚠️  Tentando estratégia alternativa com h3/h4...")
                try:
                    for tag in ["h3", "h4"]:
                        elements = self.driver.find_elements(By.TAG_NAME, tag)
                        for elem in elements[:30]:
                            try:
                                text = elem.text.strip()
                                text_lower = text.lower()
                                
                                if text and len(text) > 20 and len(text) < 200:
                                    if not any(keyword in text_lower for keyword in filter_keywords):
                                        if not text.startswith(("•", "...", "-")):
                                            headlines.append(text)
                            except:
                                continue
                except Exception as e:
                    print(f"  ✗ Erro na estratégia alternativa: {e}")
            
            # Remove duplicatas mantendo ordem
            unique_headlines = []
            seen = set()
            for h in headlines:
                h_lower = h.lower()
                if h_lower not in seen:
                    seen.add(h_lower)
                    unique_headlines.append(h)
            
            # Limita a 15 manchetes
            unique_headlines = unique_headlines[:15]
            print(f"✓ Total de manchetes únicas filtradas: {len(unique_headlines)}")
            
            # Debug: mostra as primeiras manchetes
            if unique_headlines:
                print("\n📰 Primeiras manchetes encontradas:")
                for i, h in enumerate(unique_headlines[:5], 1):
                    print(f"  {i}. {h[:80]}{'...' if len(h) > 80 else ''}")
                print()
            
            return unique_headlines
            
        except Exception as e:
            print(f"❌ Erro ao extrair notícias: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def analyze_page(self, url: str = None) -> Dict[str, any]:
        """Analisa uma página web e extrai informações estruturadas"""
        if url:
            self.open_url(url)
            time.sleep(3)
        
        if not self.driver:
            return {"error": "Driver não inicializado"}
        
        try:
            print(f"🔍 Analisando página: {self.driver.current_url}")
            
            analysis = {
                "url": self.driver.current_url,
                "title": self.driver.title,
                "summary": "",
                "main_content": [],
                "key_points": [],
                "metadata": {}
            }
            
            html = self.driver.page_source
            
            if BS4_AVAILABLE:
                soup = BeautifulSoup(html, 'html.parser')
                
                # Remove elementos não relevantes
                for element in soup(["script", "style", "nav", "footer", "header", "aside", "iframe"]):
                    element.decompose()
                
                # Extrai metadata
                analysis["metadata"] = {
                    "description": soup.find("meta", {"name": "description"}),
                    "keywords": soup.find("meta", {"name": "keywords"}),
                    "author": soup.find("meta", {"name": "author"}),
                    "published": soup.find("meta", {"property": "article:published_time"}),
                }
                
                # Processa metadata
                for key in analysis["metadata"]:
                    tag = analysis["metadata"][key]
                    if tag:
                        analysis["metadata"][key] = tag.get("content", tag.get("property", ""))
                    else:
                        analysis["metadata"][key] = ""
                
                # Extrai conteúdo principal
                # Procura por tags de artigo/main
                main_content = soup.find('article') or soup.find('main') or soup.find('div', class_=lambda x: x and 'content' in x.lower())
                
                if main_content:
                    # Extrai parágrafos do conteúdo principal
                    paragraphs = main_content.find_all('p')
                    for p in paragraphs:
                        text = p.get_text(strip=True)
                        if len(text) > 50:  # Apenas parágrafos substanciais
                            analysis["main_content"].append(text)
                    
                    # Extrai listas (pontos-chave)
                    lists = main_content.find_all(['ul', 'ol'])
                    for lst in lists:
                        items = lst.find_all('li')
                        for item in items:
                            text = item.get_text(strip=True)
                            if len(text) > 10:
                                analysis["key_points"].append(text)
                
                # Se não encontrou conteúdo principal, tenta pegar todos os parágrafos
                if not analysis["main_content"]:
                    paragraphs = soup.find_all('p')
                    for p in paragraphs:
                        text = p.get_text(strip=True)
                        if len(text) > 50:
                            analysis["main_content"].append(text)
                
                # Limita tamanho
                analysis["main_content"] = analysis["main_content"][:15]
                analysis["key_points"] = analysis["key_points"][:10]
                
                # Cria resumo
                if analysis["metadata"]["description"]:
                    analysis["summary"] = analysis["metadata"]["description"]
                elif analysis["main_content"]:
                    analysis["summary"] = analysis["main_content"][0][:300] + "..."
                
                print(f"✓ Análise completa: {len(analysis['main_content'])} parágrafos, {len(analysis['key_points'])} pontos-chave")
                
            else:
                # Fallback sem BeautifulSoup
                body = self.driver.find_element(By.TAG_NAME, "body")
                analysis["summary"] = body.text[:500]
            
            return analysis
            
        except Exception as e:
            print(f"❌ Erro na análise: {e}")
            import traceback
            traceback.print_exc()
            return {"error": str(e)}
    
    def find_clickable_elements(self) -> List[Dict]:
        """Encontra elementos clicáveis na página"""
        if not self.driver:
            return []
        
        try:
            elements = []
            
            # Busca botões
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            for btn in buttons[:20]:
                try:
                    text = btn.text.strip()
                    if text:
                        elements.append({
                            "type": "button",
                            "text": text,
                            "element": btn,
                            "visible": btn.is_displayed()
                        })
                except:
                    continue
            
            # Busca links
            links = self.driver.find_elements(By.TAG_NAME, "a")
            for link in links[:30]:
                try:
                    text = link.text.strip()
                    if text and len(text) > 3:
                        elements.append({
                            "type": "link",
                            "text": text,
                            "element": link,
                            "visible": link.is_displayed()
                        })
                except:
                    continue
            
            return elements
            
        except Exception as e:
            print(f"Erro ao buscar elementos: {e}")
            return []
    
    def click_element(self, text: str) -> bool:
        """Clica em um elemento pela descrição de texto"""
        if not self.driver:
            print("❌ Driver não inicializado")
            return False
        
        try:
            print(f"🖱️  Procurando elemento com texto: '{text}'")
            
            # Tenta encontrar por texto exato em botões
            try:
                button = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, f"//button[contains(., '{text}')]"))
                )
                button.click()
                print(f"✓ Clicou no botão: '{text}'")
                return True
            except TimeoutException:
                pass
            
            # Tenta encontrar por texto exato em links
            try:
                link = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, f"//a[contains(., '{text}')]"))
                )
                link.click()
                print(f"✓ Clicou no link: '{text}'")
                return True
            except TimeoutException:
                pass
            
            # Tenta busca parcial (case-insensitive)
            text_lower = text.lower()
            clickables = self.find_clickable_elements()
            
            for item in clickables:
                if item['visible'] and text_lower in item['text'].lower():
                    try:
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", item['element'])
                        time.sleep(0.5)
                        item['element'].click()
                        print(f"✓ Clicou em {item['type']}: '{item['text']}'")
                        return True
                    except Exception as e:
                        print(f"  Tentativa de clicar falhou: {e}")
                        continue
            
            print(f"✗ Não encontrei elemento com texto: '{text}'")
            return False
            
        except Exception as e:
            print(f"❌ Erro ao clicar: {e}")
            return False
    
    def type_text(self, selector: str, text: str) -> bool:
        """Digita texto em um campo de input"""
        if not self.driver:
            return False
        
        try:
            element = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            element.clear()
            element.send_keys(text)
            print(f"✓ Texto digitado em: {selector}")
            return True
        except Exception as e:
            print(f"✗ Erro ao digitar: {e}")
            return False
    
    def scroll_page(self, direction: str = "down", amount: int = 500):
        """Rola a página"""
        if not self.driver:
            return False
        
        try:
            if direction == "down":
                self.driver.execute_script(f"window.scrollBy(0, {amount});")
            elif direction == "up":
                self.driver.execute_script(f"window.scrollBy(0, -{amount});")
            elif direction == "bottom":
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            elif direction == "top":
                self.driver.execute_script("window.scrollTo(0, 0);")
            
            time.sleep(0.5)
            print(f"✓ Página rolada: {direction}")
            return True
        except Exception as e:
            print(f"✗ Erro ao rolar: {e}")
            return False
    
    def get_interactive_elements(self) -> str:
        """Retorna descrição dos elementos interativos visíveis"""
        elements = self.find_clickable_elements()
        visible = [e for e in elements if e['visible']][:15]
        
        if not visible:
            return "Nenhum elemento interativo encontrado"
        
        result = "Elementos clicáveis disponíveis:\n"
        for i, elem in enumerate(visible, 1):
            result += f"{i}. [{elem['type']}] {elem['text']}\n"
        
        return result
    
    def search_google(self, query: str) -> bool:
        """Realiza busca no Google e aguarda resultados"""
        try:
            if not self.driver:
                return False
            
            # Se não estiver no Google, abre
            current_url = self.driver.current_url if self.driver else ""
            if "google.com" not in current_url:
                self.driver.get("https://www.google.com")
                time.sleep(2)
            
            # Procura pela caixa de pesquisa
            search_box = None
            try:
                search_box = self.driver.find_element(By.NAME, "q")
            except:
                try:
                    search_box = self.driver.find_element(By.CSS_SELECTOR, "textarea[name='q']")
                except:
                    try:
                        search_box = self.driver.find_element(By.CSS_SELECTOR, "input[name='q']")
                    except:
                        pass
            
            if search_box:
                # Limpa e digita a busca
                search_box.clear()
                search_box.send_keys(query)
                search_box.send_keys(Keys.RETURN)
                
                # Aguarda resultados carregarem
                time.sleep(3)
                print(f"✓ Busca realizada: {query}")
                return True
            else:
                print("✗ Caixa de pesquisa não encontrada")
                return False
                
        except Exception as e:
            print(f"✗ Erro ao buscar: {e}")
            return False
    
    def close(self):
        """Fecha o navegador"""
        if self.driver:
            try:
                self.driver.quit()
                print("✓ Navegador fechado")
            except:
                pass
            self.driver = None
    
    def close_tab(self):
        """Fecha a aba atual do navegador"""
        if not self.driver:
            return False
        
        try:
            # Se houver múltiplas abas, fecha a atual
            if len(self.driver.window_handles) > 1:
                self.driver.close()
                # Muda para a última aba
                self.driver.switch_to.window(self.driver.window_handles[-1])
                print("✓ Aba fechada")
            else:
                # Se for a única aba, fecha o navegador
                self.close()
            return True
        except Exception as e:
            print(f"✗ Erro ao fechar aba: {e}")
            return False
    
    def run_system_command(self, command: str) -> Dict:
        """Executa comando do sistema"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'Comando expirou (timeout)'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def take_screenshot(self, filename: str = None) -> str:
        """Tira screenshot da tela"""
        try:
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_{timestamp}.png"
            
            screenshot = pyautogui.screenshot()
            screenshot.save(filename)
            print(f"✓ Screenshot salvo: {filename}")
            return filename
        except Exception as e:
            print(f"✗ Erro ao tirar screenshot: {e}")
            return None
    
    def press_key(self, key: str):
        """Pressiona uma tecla"""
        try:
            pyautogui.press(key)
            print(f"✓ Tecla pressionada: {key}")
            return True
        except Exception as e:
            print(f"✗ Erro ao pressionar tecla: {e}")
            return False
    
    def type_text(self, text: str):
        """Digita texto usando pyautogui"""
        try:
            pyautogui.write(text, interval=0.05)
            print(f"✓ Texto digitado: {text[:50]}...")
            return True
        except Exception as e:
            print(f"✗ Erro ao digitar texto: {e}")
            return False
    
    def click_position(self, x: int, y: int):
        """Clica em uma posição da tela"""
        try:
            pyautogui.click(x, y)
            print(f"✓ Clique em posição ({x}, {y})")
            return True
        except Exception as e:
            print(f"✗ Erro ao clicar: {e}")
            return False


class ChatInterface:
    """Interface gráfica para chat com Ollama"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Obelisk - Agente Autônomo AI")
        self.root.geometry("1000x750")
        
        # Inicializa componentes
        self.ollama = OllamaChat(BASE_URL, MODEL)
        self.browser = BrowserController()
        self.agent = AutonomousAgent(BASE_URL, MODEL)
        
        # Inicializa processador de intenções
        if INTENT_PROCESSOR_AVAILABLE:
            self.intent_processor = IntentProcessor()
        else:
            self.intent_processor = None
        
        # Estado do agente
        self.autonomous_mode = False
        self.agent_running = False
        
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
            text="🤖 Obelisk Chat + Web Vision",
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
        
        # Botão Modo Autônomo
        self.auto_button = tk.Button(
            button_frame,
            text="🤖 Modo Autônomo",
            command=self.toggle_autonomous_mode,
            bg="#059669",
            fg=self.fg_color,
            font=("Segoe UI", 9, "bold"),
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor="hand2"
        )
        self.auto_button.pack(fill=tk.X, pady=(0, 5))
        
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
        selenium_status = "✓ Disponível (abre sob demanda)" if SELENIUM_AVAILABLE else "✗ Desabilitado (instale selenium)"
        welcome = f"""Bem-vindo ao Obelisk - Agente Autônomo AI! 🤖🚀

═══════════════════════════════════════════════════════
🎯 MODO AUTÔNOMO - AGENTE 100% INDEPENDENTE
═══════════════════════════════════════════════════════

Este agente pode:
✅ VER sua tela em tempo real (captura contínua)
✅ PLANEJAR etapas para completar tarefas
✅ EXECUTAR ações automaticamente (click, type, search)
✅ SE ADAPTAR conforme resultados
✅ Navegar na web e extrair informações
✅ Controlar aplicativos e sistema

🤖 MODO AUTÔNOMO:
Clique em "🤖 Modo Autônomo" para ativar!
Quando ativo, o agente irá:
1. Ver sua tela constantemente
2. Planejar os passos necessários
3. Executar cada ação automaticamente
4. Adaptar-se aos resultados
5. Reportar o progresso em tempo real

Automação Web: {selenium_status}

💡 Exemplos de uso no Modo Autônomo:
"Pesquise pela votação do GOTY e me diga quem ganhou"
"Abra o YouTube e encontre vídeos sobre Python"
"Crie um documento no Bloco de Notas com minha lista de tarefas"
"Tire prints da tela e salve com timestamp"
"Abra a calculadora e calcule 123 * 456"

📋 Comandos especiais (modo normal):
• /news - Abre Google Notícias
• /browser <url> - Abre URL
• /analyze <url> - Analisa página
• /clear - Limpa o chat
• /reset - Reinicia conversa

⚠️ IMPORTANTE:
O modo autônomo tem controle TOTAL do seu computador!
Use apenas para tarefas que você confia.

Digite sua mensagem e pressione Enter para começar!
"""
        self.add_message("Sistema", welcome, "system")
    
    def add_system_message(self, text: str):
        """Adiciona mensagem do sistema rapidamente"""
        self.chat_display.config(state=tk.NORMAL)
        if self.chat_display.get("1.0", tk.END).strip():
            self.chat_display.insert(tk.END, "\n")
        self.chat_display.insert(tk.END, f"[Sistema] {text}\n", "system")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        self.root.update()
        
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
        self.root.update()
        
    def process_command(self, message: str) -> Optional[str]:
        """Processa comandos especiais"""
        message = message.strip()
        
        if message.startswith('/browser '):
            url = message[9:].strip()
            # Inicializa navegador se necessário
            if not self.browser.driver and SELENIUM_AVAILABLE:
                self.add_system_message("🔄 Iniciando navegador Chrome...")
                if not self.browser.initialize_driver():
                    return "✗ Não foi possível inicializar o navegador"
                self.add_system_message("✓ Chrome pronto!")
            
            if self.browser.open_url(url):
                return f"✓ Navegador aberto: {url}"
            else:
                return f"✗ Erro ao abrir: {url}"
        
        elif message.startswith('/analyze '):
            url = message[9:].strip()
            # Inicializa navegador se necessário
            if not self.browser.driver and SELENIUM_AVAILABLE:
                self.add_system_message("🔄 Iniciando navegador Chrome...")
                if not self.browser.initialize_driver():
                    return "✗ Não foi possível inicializar o navegador"
                self.add_system_message("✓ Chrome pronto!")
            
            if not self.browser.driver:
                return "✗ Selenium não disponível"
            
            self.add_system_message(f"🔍 Analisando {url}...")
            analysis = self.browser.analyze_page(url)
            
            if "error" in analysis:
                return f"✗ Erro: {analysis['error']}"
            
            result = f"📄 Análise de: {analysis['title']}\n\n"
            if analysis['summary']:
                result += f"📝 Resumo:\n{analysis['summary']}\n\n"
            if analysis['key_points']:
                result += "🔑 Pontos-chave:\n"
                for point in analysis['key_points'][:5]:
                    result += f"• {point}\n"
                result += "\n"
            if analysis['main_content']:
                result += f"📖 Conteúdo principal:\n{analysis['main_content'][0][:500]}...\n"
            
            return result
        
        elif message == '/news':
            # Inicializa navegador se necessário
            if not self.browser.driver and SELENIUM_AVAILABLE:
                self.add_system_message("🔄 Iniciando navegador Chrome...")
                if not self.browser.initialize_driver():
                    return "✗ Não foi possível inicializar o navegador"
                self.add_system_message("✓ Chrome pronto!")
            
            if not self.browser.driver:
                return "✗ Selenium não disponível. Instale com: pip install selenium"
            
            self.add_system_message("🔍 Acessando Google Notícias...")
            headlines = self.browser.get_google_news_headlines()
            if headlines:
                result = "📰 Manchetes do Google Notícias:\n\n"
                for i, headline in enumerate(headlines, 1):
                    result += f"{i}. {headline}\n"
                return result
            else:
                return "✗ Não foi possível extrair manchetes. Veja o terminal para detalhes."
        
        elif message == '/page':
            content = self.browser.get_page_content()
            if "error" in content:
                return f"✗ Erro: {content['error']}"
            result = f"📄 Página: {content['title']}\nURL: {content['url']}\n\n"
            if content['headlines']:
                result += "Manchetes encontradas:\n"
                for h in content['headlines'][:5]:
                    result += f"• {h}\n"
            return result
        
        elif message.startswith('/click '):
            text = message[7:].strip()
            if not self.browser.driver:
                return "✗ Abra uma página primeiro com /browser <url>"
            
            self.add_system_message(f"🖱️  Clicando em: '{text}'...")
            if self.browser.click_element(text):
                time.sleep(1.5)
                return f"✓ Clicado em: {text}"
            else:
                elements = self.browser.get_interactive_elements()
                return f"✗ Não encontrei: {text}\n\n{elements}"
        
        elif message.startswith('/scroll '):
            direction = message[8:].strip().lower()
            if not self.browser.driver:
                return "✗ Abra uma página primeiro"
            
            if self.browser.scroll_page(direction):
                return f"✓ Página rolada: {direction}"
            else:
                return "✗ Use: up, down, top, bottom"
        
        elif message == '/elements':
            if not self.browser.driver:
                return "✗ Abra uma página primeiro"
            return self.browser.get_interactive_elements()
                
        elif message == '/clear':
            self.clear_chat()
            return None
            
        elif message == '/reset':
            self.ollama.reset()
            return "✓ Conversa reiniciada"
            
        return None
        
    def execute_intent_action(self, user_message: str) -> Optional[str]:
        """Detecta e executa ações automaticamente baseadas na intenção do usuário
        
        Retorna contexto da ação executada para o Ollama ou None se não executou nada.
        """
        if not self.intent_processor:
            return None
        
        # Detecta intenção
        intent = self.intent_processor.detect_intent(user_message)
        
        # Se confiança muito baixa, deixa o Ollama processar
        if intent['confianca'] < 0.6:
            return None
        
        # Mostra ao usuário o que foi detectado
        explanation = self.intent_processor.explain_intent(intent)
        self.add_system_message(f"🧠 {explanation}")
        self.root.update()
        
        acao = intent['acao']
        params = intent['parametros']
        
        # Executa ação correspondente
        if acao == 'OPEN_BROWSER':
            return self._execute_open_browser(params)
        
        elif acao == 'SEARCH':
            return self._execute_search(params)
        
        elif acao == 'NEWS_SUMMARY':
            return self._execute_news_summary(params)
        
        elif acao == 'SCREENSHOT':
            return self._execute_screenshot(params)
        
        elif acao == 'CLOSE_BROWSER':
            return self._execute_close_browser(params)
        
        elif acao == 'CLOSE_TAB':
            return self._execute_close_tab(params)
        
        elif acao == 'OPEN_APP':
            return self._execute_open_app(params)
        
        # Ação não reconhecida ou CHAT - deixa para o Ollama
        return None
    
    def _execute_open_browser(self, params: Dict) -> str:
        """Executa abertura de navegador"""
        url = params['url']
        nome = params['nome']
        
        # Inicializa navegador se necessário
        if not self.browser.driver and SELENIUM_AVAILABLE:
            self.add_system_message("🔄 Iniciando navegador Chrome...")
            self.root.update()
            if not self.browser.initialize_driver():
                self.add_system_message("✗ Não foi possível inicializar o navegador")
                return f"CONTEXTO: Você tentou abrir {nome} mas o navegador não está disponível."
            self.add_system_message("✓ Chrome pronto!")
        
        if not self.browser.driver:
            return f"CONTEXTO: Navegador não disponível."
        
        # Abre URL
        self.add_system_message(f"🌐 Abrindo {nome}...")
        self.root.update()
        
        self.browser.open_url(url)
        time.sleep(2)
        
        # Analisa conteúdo
        content = self.browser.get_page_content()
        
        if content and "error" not in content:
            context = f"CONTEXTO: Você acabou de abrir {nome} ({url})\n"
            context += f"Título da página: {content['title']}\n\n"
            
            if content.get('headlines'):
                context += "Títulos visíveis na página:\n"
                for i, h in enumerate(content['headlines'][:8], 1):
                    if isinstance(h, dict):
                        context += f"{i}. {h.get('text', '')}\n"
                    else:
                        context += f"{i}. {h}\n"
                context += "\n"
            
            if content.get('paragraphs'):
                context += f"Conteúdo: {len(content['paragraphs'])} parágrafos\n"
                context += f"Primeiro trecho: {content['paragraphs'][0][:200]}...\n\n"
            
            context += "Informe ao usuário que você abriu o site e o que viu lá."
            return context
        
        return f"CONTEXTO: Você abriu {nome} em {url}"
    
    def _execute_search(self, params: Dict) -> str:
        """Executa busca no Google"""
        query = params['query']
        
        # Inicializa navegador
        if not self.browser.driver and SELENIUM_AVAILABLE:
            self.add_system_message("🔄 Iniciando navegador Chrome...")
            self.root.update()
            if not self.browser.initialize_driver():
                return f"CONTEXTO: Navegador não disponível para pesquisar '{query}'."
            self.add_system_message("✓ Chrome pronto!")
        
        if not self.browser.driver:
            return f"CONTEXTO: Não conseguiu pesquisar '{query}'."
        
        # Faz busca
        self.add_system_message(f"🔍 Pesquisando '{query}' no Google...")
        self.root.update()
        
        self.browser.search_google(query)
        time.sleep(2)
        
        # Analisa resultados
        content = self.browser.get_page_content()
        elements = self.browser.get_interactive_elements()
        
        if content and "error" not in content:
            context = f"CONTEXTO: Você pesquisou '{query}' no Google.\n\n"
            context += f"RESULTADOS ENCONTRADOS:\n"
            
            if content.get('headlines'):
                context += "Títulos dos resultados:\n"
                for i, h in enumerate(content['headlines'][:10], 1):
                    if isinstance(h, dict):
                        text = h.get('text', '')
                        if len(text) > 20:  # Filtra títulos muito curtos
                            context += f"{i}. {text}\n"
                context += "\n"
            
            if content.get('paragraphs'):
                context += "Descrições dos resultados:\n"
                for i, p in enumerate(content['paragraphs'][:5], 1):
                    if len(p) > 50:
                        context += f"{i}. {p[:200]}...\n"
                context += "\n"
            
            context += f"Elementos clicáveis:\n{elements[:500]}\n\n"
            context += f"Você realizou a busca com sucesso. Informe ao usuário o que encontrou sobre '{query}'."
            
            return context
        
        return f"CONTEXTO: Você pesquisou '{query}' no Google."
    
    def _execute_news_summary(self, params: Dict) -> str:
        """Executa resumo de notícias"""
        sites = params['sites']
        
        self.add_system_message("📰 Coletando notícias dos principais sites...")
        self.root.update()
        
        # Inicializa navegador
        if not self.browser.driver and SELENIUM_AVAILABLE:
            self.add_system_message("🔄 Iniciando navegador...")
            self.root.update()
            if not self.browser.initialize_driver():
                return "CONTEXTO: Não foi possível abrir navegador para coletar notícias."
            self.add_system_message("✓ Chrome pronto!")
        
        # Coleta manchetes
        all_headlines = []
        
        for site_url in sites[:2]:  # Limita a 2 sites para não demorar
            self.add_system_message(f"🌐 Acessando {site_url}...")
            self.root.update()
            
            self.browser.open_url(site_url)
            time.sleep(3)
            
            content = self.browser.get_page_content()
            if content and content.get('headlines'):
                for h in content['headlines'][:10]:
                    if isinstance(h, dict):
                        text = h.get('text', '')
                    else:
                        text = h
                    
                    if len(text) > 20:  # Filtra curtos
                        all_headlines.append(text)
        
        if all_headlines:
            context = "CONTEXTO: Você coletou as principais notícias:\n\n"
            context += "MANCHETES:\n"
            for i, headline in enumerate(all_headlines[:15], 1):
                context += f"{i}. {headline}\n"
            context += "\nFaça um resumo das principais notícias para o usuário."
            return context
        
        return "CONTEXTO: Você tentou coletar notícias mas não encontrou manchetes."
    
    def _execute_screenshot(self, params: Dict) -> str:
        """Tira screenshot"""
        self.add_system_message("📸 Capturando tela...")
        self.root.update()
        
        try:
            screenshot = pyautogui.screenshot()
            filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            screenshot.save(filename)
            
            self.add_system_message(f"✓ Screenshot salvo: {filename}")
            return f"CONTEXTO: Você tirou um screenshot e salvou como '{filename}'. Informe ao usuário."
        except Exception as e:
            return f"CONTEXTO: Erro ao tirar screenshot: {e}"
    
    def _execute_close_browser(self, params: Dict) -> str:
        """Fecha navegador"""
        if self.browser.driver:
            self.add_system_message("🔴 Fechando navegador...")
            self.root.update()
            self.browser.close()
            return "CONTEXTO: Você fechou o navegador. Informe ao usuário."
        return "CONTEXTO: O navegador já estava fechado."
    
    def _execute_close_tab(self, params: Dict) -> str:
        """Fecha aba atual"""
        if self.browser.driver:
            self.add_system_message("🔴 Fechando aba...")
            self.root.update()
            self.browser.close_tab()
            
            if self.browser.driver:
                try:
                    current_url = self.browser.driver.current_url
                    return f"CONTEXTO: Você fechou a aba. Agora está vendo: {current_url}"
                except:
                    return "CONTEXTO: Você fechou a aba."
            return "CONTEXTO: Você fechou o navegador (era a última aba)."
        return "CONTEXTO: Não há navegador aberto."
    
    def _execute_open_app(self, params: Dict) -> str:
        """Abre programa"""
        app = params['app']
        nome = params['nome']
        
        self.add_system_message(f"🚀 Abrindo {nome}...")
        self.root.update()
        
        try:
            subprocess.Popen(app, shell=True)
            time.sleep(1)
            return f"CONTEXTO: Você abriu {nome}. Informe ao usuário."
        except Exception as e:
            return f"CONTEXTO: Erro ao abrir {nome}: {e}"
    
    def check_for_web_action(self, user_message: str) -> Optional[str]:
        """Verifica se precisa executar ação web e retorna contexto"""
        
        # Inicializa navegador se necessário para qualquer ação web
        def ensure_browser():
            if not self.browser.driver and SELENIUM_AVAILABLE:
                self.add_system_message("🔄 Iniciando navegador Chrome...")
                self.root.update()
                if not self.browser.initialize_driver():
                    self.add_system_message("✗ Não foi possível inicializar o navegador")
                    return False
                self.add_system_message("✓ Chrome pronto!")
                self.root.update()
            return self.browser.driver is not None
        
        # Palavras-chave que indicam intenção de abrir sites
        open_keywords = [
            "abre", "abra", "abrir", "acesse", "acessa", "acessar",
            "visite", "visita", "visitar", "vá para", "va para", "ir para"
        ]
        
        # Sites comuns e seus URLs
        common_sites = {
            "google": "https://www.google.com",
            "youtube": "https://www.youtube.com",
            "facebook": "https://www.facebook.com",
            "twitter": "https://www.twitter.com",
            "instagram": "https://www.instagram.com",
            "linkedin": "https://www.linkedin.com",
            "github": "https://www.github.com",
            "wikipedia": "https://www.wikipedia.org",
            "reddit": "https://www.reddit.com",
            "amazon": "https://www.amazon.com.br",
            "mercado livre": "https://www.mercadolivre.com.br",
            "gmail": "https://mail.google.com",
            "google drive": "https://drive.google.com",
            "google maps": "https://maps.google.com",
        }
        
        # Palavras-chave que indicam intenção de clicar
        click_keywords = [
            "clique", "clica", "aperte", "pressione", "selecione",
            "escolha", "click"
        ]
        
        # Palavras-chave que indicam intenção de ver notícias
        news_keywords = [
            "google notícias", "google noticias", "notícias", "noticias",
            "manchetes", "última notícia", "ultimas noticias", "primeira notícia",
            "news.google", "primeira noticia", "manchete", "headline"
        ]
        
        # Palavras-chave para análise de página
        analyze_keywords = [
            "analise", "análise", "resuma", "resumo", "me fale sobre",
            "o que tem", "qual o conteúdo", "confira"
        ]
        
        # Palavras-chave para mostrar elementos
        elements_keywords = [
            "elementos", "botões", "botoes", "links", "o que posso clicar",
            "opções", "opcoes"
        ]
        
        # Palavras-chave para fechar
        close_keywords = [
            "fecha", "feche", "fechar", "sai do", "saia do", "sair do"
        ]
        
        # Alvos de fechamento
        close_targets = {
            "navegador": ["navegador", "chrome", "browser"],
            "aba": ["aba", "tab", "página", "pagina"],
            "google": ["google"],
            "site": ["site", "página", "pagina"]
        }
        
        # Palavras-chave que indicam busca/pesquisa
        search_keywords = [
            "pesquise", "pesquisa", "busque", "busca", "procure", "procura",
            "encontre", "encontra", "pesquisar", "buscar", "procurar", "encontrar",
            "me mostre", "me mostra", "quero ver", "me diga sobre", "me fale sobre"
        ]
        
        lower_message = user_message.lower()
        
        # BUSCA INTELIGENTE - Detecta intenção de pesquisar
        if any(keyword in lower_message for keyword in search_keywords):
            # Extrai o termo de busca
            search_query = None
            
            # Padrões para extrair query
            patterns = [
                r'(?:pesquise|pesquisa|busque|busca|procure|procura|encontre)(?:\s+por)?\s+["\']?(.+?)["\']?$',
                r'(?:pesquisar|buscar|procurar|encontrar)(?:\s+por)?\s+["\']?(.+?)["\']?$',
                r'(?:me mostre|me mostra|quero ver)(?:\s+sobre)?\s+["\']?(.+?)["\']?$',
                r'(?:me diga|me fale)(?:\s+sobre)?\s+["\']?(.+?)["\']?$',
            ]
            
            for pattern in patterns:
                match = re.search(pattern, lower_message)
                if match:
                    search_query = match.group(1).strip()
                    break
            
            # Se não conseguiu extrair com regex, pega tudo depois da palavra-chave
            if not search_query:
                for keyword in search_keywords:
                    if keyword in lower_message:
                        parts = lower_message.split(keyword, 1)
                        if len(parts) > 1:
                            search_query = parts[1].strip()
                            # Remove preposições comuns
                            for prep in ["por", "sobre", "a", "o"]:
                                if search_query.startswith(prep + " "):
                                    search_query = search_query[len(prep)+1:].strip()
                            break
            
            if search_query:
                if not ensure_browser():
                    return None
                
                self.add_system_message(f"🔍 Pesquisando: {search_query}")
                self.root.update()
                
                # Realiza a busca
                if self.browser.search_google(search_query):
                    time.sleep(2)
                    
                    # Analisa os resultados
                    content = self.browser.get_page_content()
                    elements = self.browser.get_interactive_elements()
                    
                    if content and "error" not in content:
                        context = f"AÇÃO EXECUTADA: Você acabou de pesquisar '{search_query}' no Google.\n"
                        context += f"Página de resultados: {content['title']}\n"
                        context += f"URL: {content['url']}\n\n"
                        
                        if content.get('headlines'):
                            context += "RESULTADOS DA BUSCA (primeiros 10):\n"
                            for i, h in enumerate(content['headlines'][:10], 1):
                                if isinstance(h, dict):
                                    context += f"{i}. {h.get('text', '')}\n"
                                else:
                                    context += f"{i}. {h}\n"
                            context += "\n"
                        
                        if content.get('paragraphs'):
                            context += "DESCRIÇÕES DOS RESULTADOS:\n"
                            for i, p in enumerate(content['paragraphs'][:5], 1):
                                context += f"{i}. {p[:150]}...\n"
                            context += "\n"
                        
                        context += f"ELEMENTOS CLICÁVEIS:\n{elements}\n\n"
                        context += f"Você realizou a busca com sucesso. Agora analise os resultados e informe ao usuário o que encontrou sobre '{search_query}'."
                        
                        return context
                    else:
                        return f"CONTEXTO: Você pesquisou '{search_query}' no Google mas teve dificuldade em analisar os resultados."
        
        # Detecta se pede para fechar algo
        if any(keyword in lower_message for keyword in close_keywords):
            if self.browser.driver:
                # Determina o que fechar
                if any(target in lower_message for target in close_targets["navegador"]):
                    self.add_system_message("🔴 Fechando navegador...")
                    self.root.update()
                    self.browser.close()
                    return "CONTEXTO: Você fechou o navegador Chrome completamente. Informe ao usuário que o navegador foi fechado."
                
                elif any(target in lower_message for target in close_targets["aba"] + close_targets["google"] + close_targets["site"]):
                    self.add_system_message("🔴 Fechando aba atual...")
                    self.root.update()
                    self.browser.close_tab()
                    
                    # Verifica se ainda há navegador aberto
                    if self.browser.driver:
                        try:
                            current_url = self.browser.driver.current_url
                            return f"CONTEXTO: Você fechou a aba anterior. Agora está vendo: {current_url}. Informe ao usuário."
                        except:
                            return "CONTEXTO: Você fechou a aba. Informe ao usuário."
                    else:
                        return "CONTEXTO: Você fechou o navegador (era a última aba). Informe ao usuário."
                else:
                    # Padrão: fecha a aba atual
                    self.add_system_message("🔴 Fechando aba atual...")
                    self.root.update()
                    self.browser.close_tab()
                    return "CONTEXTO: Você fechou a aba/página atual. Informe ao usuário."
        
        # Detecta se pede para abrir algum site comum
        if any(keyword in lower_message for keyword in open_keywords):
            # Procura por sites comuns
            for site, url in common_sites.items():
                if site in lower_message:
                    if not ensure_browser():
                        return None
                    
                    self.add_system_message(f"🌐 Abrindo {site.title()}...")
                    self.root.update()
                    
                    self.browser.open_url(url)
                    time.sleep(2)
                    
                    # Analisa a página
                    content = self.browser.get_page_content()
                    elements = self.browser.get_interactive_elements()
                    
                    if content and "error" not in content:
                        context = f"CONTEXTO: Você acabou de abrir {site.title()} ({url})\n"
                        context += f"Título da página: {content['title']}\n\n"
                        
                        if content.get('headlines'):
                            context += "Títulos visíveis:\n"
                            for i, h in enumerate(content['headlines'][:8], 1):
                                if isinstance(h, dict):
                                    context += f"{i}. {h.get('text', '')}\n"
                                else:
                                    context += f"{i}. {h}\n"
                            context += "\n"
                        
                        context += f"Elementos clicáveis:\n{elements}\n\n"
                        context += "Informe ao usuário que você abriu o site e está vendo o conteúdo."
                        
                        return context
                    
                    return f"CONTEXTO: Você abriu {site.title()} em {url}"
        
        # Detecta URLs na mensagem
        url_pattern = r'https?://[^\s]+|www\.[^\s]+|[a-zA-Z0-9-]+\.(com|org|net|br|gov|edu|io|dev|app)[^\s]*'
        urls = re.findall(url_pattern, user_message)
        
        # Se mencionou abrir + URL específica
        if urls and any(keyword in lower_message for keyword in open_keywords):
            url = urls[0]
            if not url.startswith('http'):
                url = 'https://' + url
            
            if not ensure_browser():
                return None
            
            self.add_system_message(f"🌐 Abrindo {url}...")
            self.root.update()
            
            self.browser.open_url(url)
            time.sleep(2)
            
            content = self.browser.get_page_content()
            elements = self.browser.get_interactive_elements()
            
            if content and "error" not in content:
                context = f"CONTEXTO: Você abriu {content['title']}\n"
                context += f"URL: {url}\n\n"
                
                if content.get('headlines'):
                    context += "Títulos:\n"
                    for h in content['headlines'][:5]:
                        if isinstance(h, dict):
                            context += f"- {h.get('text', '')}\n"
                        else:
                            context += f"- {h}\n"
                    context += "\n"
                
                context += f"Elementos clicáveis:\n{elements}"
                return context
        
        # Verifica se pede para mostrar elementos
        if any(keyword in lower_message for keyword in elements_keywords):
            if self.browser.driver:
                elements_list = self.browser.get_interactive_elements()
                self.add_message("Elementos", elements_list, "system")
                return f"CONTEXTO: Você verificou a página e encontrou os seguintes elementos clicáveis:\n{elements_list}\nResponda ao usuário sobre estes elementos."
        
        # Verifica se pede para clicar em algo
        if any(keyword in lower_message for keyword in click_keywords):
            if self.browser.driver:
                # Tenta extrair o texto para clicar
                # Padrões: "clique em X", "clica no X", "aperte o botão X"
                patterns = [
                    r'clique\s+(?:em|no|na)\s+["\']?([^"\']+)["\']?',
                    r'clica\s+(?:em|no|na)\s+["\']?([^"\']+)["\']?',
                    r'aperte\s+(?:o|a)?\s*(?:botão|link)?\s+["\']?([^"\']+)["\']?',
                    r'pressione\s+["\']?([^"\']+)["\']?',
                ]
                
                click_text = None
                for pattern in patterns:
                    match = re.search(pattern, lower_message)
                    if match:
                        click_text = match.group(1).strip()
                        break
                
                if click_text:
                    self.add_system_message(f"🖱️  Tentando clicar em: '{click_text}'")
                    self.root.update()
                    
                    if self.browser.click_element(click_text):
                        time.sleep(2)  # Aguarda página carregar
                        self.add_system_message(f"✓ Clicado com sucesso!")
                        
                        # Analisa nova página
                        content = self.browser.get_page_content()
                        if content and "error" not in content:
                            context = f"CONTEXTO: Você clicou em '{click_text}' e agora está vendo:\n"
                            context += f"Título: {content['title']}\n"
                            if content['headlines']:
                                context += "Manchetes visíveis:\n"
                                for h in content['headlines'][:5]:
                                    if isinstance(h, dict):
                                        context += f"- {h.get('text', '')}\n"
                                    else:
                                        context += f"- {h}\n"
                            return context
                    else:
                        self.add_system_message(f"✗ Não encontrei elemento com texto: '{click_text}'")
                        # Mostra elementos disponíveis
                        elements = self.browser.get_interactive_elements()
                        self.add_message("Sugestão", f"Elementos disponíveis:\n{elements}", "system")
                        return None
        
        # Detecta URLs na mensagem
        url_pattern = r'https?://[^\s]+|www\.[^\s]+|[a-zA-Z0-9-]+\.(com|org|net|br|gov|edu)[^\s]*'
        urls = re.findall(url_pattern, user_message)
        
        # Se mencionou URL com palavra de análise
        if urls and any(keyword in lower_message for keyword in analyze_keywords):
            url = urls[0]
            if not url.startswith('http'):
                url = 'https://' + url
            
            # Inicializa navegador se necessário
            if not self.browser.driver and SELENIUM_AVAILABLE:
                self.add_system_message("🔄 Iniciando navegador Chrome...")
                self.root.update()
                if not self.browser.initialize_driver():
                    self.add_system_message("✗ Não foi possível inicializar o navegador")
                    return None
                self.add_system_message("✓ Chrome pronto!")
                self.root.update()
            
            if not self.browser.driver:
                self.add_system_message("✗ Navegador não disponível")
                return None
            
            self.add_system_message(f"🔍 Analisando {url}...")
            self.root.update()
            
            analysis = self.browser.analyze_page(url)
            
            if analysis and "error" not in analysis:
                # Cria contexto rico para o LLM
                context = f"CONTEXTO: Você acabou de acessar e analisar a página: {analysis['title']}\n"
                context += f"URL: {analysis['url']}\n\n"
                
                if analysis['summary']:
                    context += f"RESUMO: {analysis['summary']}\n\n"
                
                if analysis['key_points']:
                    context += "PONTOS-CHAVE:\n"
                    for i, point in enumerate(analysis['key_points'][:10], 1):
                        context += f"{i}. {point}\n"
                    context += "\n"
                
                if analysis['main_content']:
                    context += "CONTEÚDO PRINCIPAL:\n"
                    for i, para in enumerate(analysis['main_content'][:5], 1):
                        context += f"Parágrafo {i}: {para}\n"
                    context += "\n"
                
                context += "Responda à pergunta do usuário baseado nesta análise da página que você acabou de ver."
                
                # Mostra resumo para o usuário
                result = f"📄 {analysis['title']}\n\n"
                if analysis['summary']:
                    result += f"📝 {analysis['summary'][:300]}...\n\n"
                if analysis['key_points']:
                    result += f"🔑 {len(analysis['key_points'])} pontos-chave identificados\n"
                if analysis['main_content']:
                    result += f"📖 {len(analysis['main_content'])} seções de conteúdo extraídas"
                
                self.add_message("Web Analysis", result, "system")
                
                return context
            else:
                self.add_system_message("✗ Não consegui analisar a página")
                return None
        
        # Verifica se pede notícias (mantém lógica anterior)
        if any(keyword in lower_message for keyword in news_keywords):
            # Inicializa o navegador se ainda não foi inicializado
            if not self.browser.driver and SELENIUM_AVAILABLE:
                self.add_system_message("🔄 Iniciando navegador Chrome...")
                self.root.update()
                if not self.browser.initialize_driver():
                    self.add_system_message("✗ Não foi possível inicializar o navegador")
                    return None
                self.add_system_message("✓ Chrome pronto!")
                self.root.update()
            
            if not self.browser.driver:
                self.add_system_message("✗ Navegador não disponível. Instale: pip install selenium")
                return None
            
            self.add_system_message("🔍 Acessando Google Notícias...")
            self.root.update()
            
            headlines = self.browser.get_google_news_headlines()
            
            if headlines and len(headlines) > 0:
                # Cria contexto para o LLM
                context = "CONTEXTO IMPORTANTE: Você acabou de abrir o Google Notícias (news.google.com) no navegador e conseguiu VER as seguintes manchetes em ordem:\n\n"
                for i, headline in enumerate(headlines, 1):
                    context += f"{i}. {headline}\n"
                context += "\nESSAS SÃO AS MANCHETES REAIS QUE VOCÊ ESTÁ VENDO AGORA. Responda à pergunta do usuário baseado EXATAMENTE nestas manchetes que você viu. A primeira notícia é o item número 1."
                
                # Mostra para o usuário também
                result = "📰 Manchetes que estou vendo no Google Notícias:\n\n"
                for i, headline in enumerate(headlines, 1):
                    result += f"{i}. {headline}\n"
                self.add_message("Web Vision", result, "system")
                
                # Adiciona elementos clicáveis
                elements = self.browser.get_interactive_elements()
                context += f"\n\nELEMENTOS CLICÁVEIS DISPONÍVEIS:\n{elements}"
                
                return context
            else:
                self.add_system_message("✗ Não consegui extrair manchetes. Veja o terminal para detalhes.")
                return None
        
        # SE CHEGOU AQUI: Não é caso específico, usa análise universal
        # Verifica se já tem uma página aberta
        if self.browser.driver:
            try:
                # Analisa a página atual automaticamente
                current_url = self.browser.driver.current_url
                if current_url and current_url != "data:," and "about:blank" not in current_url:
                    self.add_system_message("🔍 Analisando página atual...")
                    self.root.update()
                    
                    # Pega conteúdo da página
                    content = self.browser.get_page_content()
                    elements = self.browser.get_interactive_elements()
                    
                    if content and "error" not in content:
                        context = f"CONTEXTO: Você está vendo a página: {content['title']}\n"
                        context += f"URL: {content['url']}\n\n"
                        
                        if content.get('headlines'):
                            context += "TÍTULOS VISÍVEIS:\n"
                            for h in content['headlines'][:10]:
                                if isinstance(h, dict):
                                    context += f"- {h.get('text', '')}\n"
                                else:
                                    context += f"- {h}\n"
                            context += "\n"
                        
                        if content.get('paragraphs'):
                            context += "CONTEÚDO PRINCIPAL:\n"
                            for i, p in enumerate(content['paragraphs'][:5], 1):
                                context += f"{i}. {p[:200]}...\n"
                            context += "\n"
                        
                        context += f"ELEMENTOS CLICÁVEIS:\n{elements}\n\n"
                        context += "Responda à pergunta do usuário baseado no conteúdo e elementos que você está vendo nesta página."
                        
                        return context
            except Exception as e:
                # Navegador foi fechado ou sessão inválida
                print(f"⚠️  Sessão do navegador inválida: {e}")
                self.browser.driver = None
                return None
        
        # Detecta comandos de sistema
        # Screenshot
        if any(word in lower_message for word in ["screenshot", "print", "captura", "tira um print", "tire um print"]):
            self.add_system_message("📸 Tirando screenshot...")
            self.root.update()
            filename = self.browser.take_screenshot()
            if filename:
                return f"CONTEXTO: Você tirou um screenshot da tela e salvou em '{filename}'. Informe ao usuário que a captura foi feita com sucesso."
            else:
                return "CONTEXTO: Tentou tirar screenshot mas ocorreu um erro. Informe ao usuário."
        
        # Executar programas (cuidado com segurança!)
        if "abra o" in lower_message or "abre o" in lower_message or "execute" in lower_message:
            # Programas comuns no Windows
            programs = {
                "bloco de notas": "notepad",
                "notepad": "notepad",
                "calculadora": "calc",
                "paint": "mspaint",
                "explorador": "explorer",
                "explorer": "explorer",
                "cmd": "cmd",
                "prompt": "cmd",
                "powershell": "powershell",
            }
            
            for prog_name, prog_cmd in programs.items():
                if prog_name in lower_message:
                    self.add_system_message(f"🚀 Abrindo {prog_name}...")
                    self.root.update()
                    result = self.browser.run_system_command(prog_cmd)
                    if result.get('success'):
                        return f"CONTEXTO: Você abriu o programa '{prog_name}' com sucesso. Informe ao usuário."
                    else:
                        return f"CONTEXTO: Tentou abrir '{prog_name}' mas ocorreu um erro. Informe ao usuário."
        
        return None
        
    def send_message(self):
        """Envia mensagem para o Ollama"""
        message = self.message_entry.get("1.0", tk.END).strip()
        
        if not message:
            return
            
        # Limpa o campo de entrada
        self.message_entry.delete("1.0", tk.END)
        
        # Adiciona mensagem do usuário
        self.add_message("Você", message, "user")
        
        # MODO AUTÔNOMO: Executa tarefa de forma completamente autônoma
        if self.autonomous_mode and not message.startswith('/'):
            self.run_autonomous_task(message)
            return
        
        # Processa comandos especiais
        command_result = self.process_command(message)
        if command_result:
            self.add_message("Sistema", command_result, "system")
            if message.startswith('/clear') or message.startswith('/reset'):
                return
        
        # Se não for comando, envia para Ollama
        if not message.startswith('/'):
            # Desabilita botão durante processamento
            self.send_button.config(state=tk.DISABLED, text="Pensando...")
            
            def get_response():
                # NOVO: Tenta detectar e executar intenção automaticamente
                web_context = None
                if self.intent_processor:
                    web_context = self.execute_intent_action(message)
                
                # Se não executou ação automática, verifica ações web tradicionais
                if not web_context:
                    web_context = self.check_for_web_action(message)
                
                # Se não gerou contexto específico, mas tem navegador aberto, adiciona contexto da página atual
                if not web_context and self.browser.driver:
                    try:
                        current_url = self.browser.driver.current_url
                        if current_url and current_url != "data:," and "about:blank" not in current_url:
                            content = self.browser.get_page_content()
                            elements = self.browser.get_interactive_elements()
                            
                            if content and "error" not in content:
                                web_context = f"CONTEXTO VISUAL: Você está com uma página aberta no navegador:\n"
                                web_context += f"Título: {content['title']}\n"
                                web_context += f"URL: {content['url']}\n\n"
                                
                                if content.get('headlines'):
                                    web_context += "Títulos visíveis (primeiros 5):\n"
                                    for i, h in enumerate(content['headlines'][:5], 1):
                                        if isinstance(h, dict):
                                            web_context += f"{i}. {h.get('text', '')}\n"
                                        else:
                                            web_context += f"{i}. {h}\n"
                                    web_context += "\n"
                                
                                if content.get('paragraphs'):
                                    web_context += f"Conteúdo: {len(content['paragraphs'])} seções de texto\n"
                                    web_context += f"Primeiro parágrafo: {content['paragraphs'][0][:300]}...\n\n"
                                
                                web_context += f"Elementos clicáveis:\n{elements}\n\n"
                                web_context += "Use este contexto para responder se a pergunta for sobre a página, seus elementos ou conteúdo."
                    except:
                        pass
                
                # Envia para Ollama com contexto se houver
                response = self.ollama.send_message(message, context=web_context)
                
                # Adiciona resposta
                self.add_message("Assistente", response, "assistant")
                
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
    
    def toggle_autonomous_mode(self):
        """Ativa/desativa modo autônomo"""
        self.autonomous_mode = not self.autonomous_mode
        
        if self.autonomous_mode:
            self.auto_button.config(
                text="🤖 MODO ATIVO",
                bg="#dc2626"
            )
            self.add_system_message("🤖 MODO AUTÔNOMO ATIVADO")
            self.add_system_message("💡 Agora eu vou VER sua tela e EXECUTAR ações automaticamente!")
            self.add_system_message("💡 Digite uma tarefa e eu vou planejar e executar todos os passos!")
        else:
            self.auto_button.config(
                text="🤖 Modo Autônomo",
                bg="#059669"
            )
            self.add_system_message("⏸️ Modo autônomo desativado")
    
    def run_autonomous_task(self, task: str):
        """Executa tarefa no modo autônomo"""
        self.agent_running = True
        self.send_button.config(state=tk.DISABLED)
        
        def progress_update(message: str):
            """Callback para atualizar progresso"""
            self.add_system_message(message)
            self.root.update()
        
        def execute_task():
            try:
                self.add_system_message(f"🎯 INICIANDO TAREFA AUTÔNOMA: {task}")
                self.add_system_message("=" * 60)
                
                # Executa tarefa autônoma
                steps = self.agent.run_autonomous_task(task, progress_update)
                
                # Reporta conclusão
                self.add_system_message("=" * 60)
                self.add_system_message("✅ TAREFA FINALIZADA!")
                self.add_system_message(f"📊 Total de passos executados: {len(steps)}")
                
                # Gera resumo com Ollama
                summary_context = f"TAREFA SOLICITADA: {task}\n\n"
                summary_context += "PASSOS EXECUTADOS:\n"
                for i, step in enumerate(steps, 1):
                    summary_context += f"{i}. {step}\n"
                summary_context += "\nGere um resumo do que foi feito e informe ao usuário o resultado."
                
                response = self.ollama.send_message(
                    "Resuma o que você acabou de fazer nesta tarefa autônoma",
                    context=summary_context
                )
                
                self.add_message("Agente", response, "assistant")
                
            except Exception as e:
                self.add_system_message(f"❌ Erro na execução: {e}")
            
            finally:
                self.agent_running = False
                self.send_button.config(state=tk.NORMAL)
        
        # Executa em thread separada
        threading.Thread(target=execute_task, daemon=True).start()
            
    def clear_chat(self):
        """Limpa o chat"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete("1.0", tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self.show_welcome_message()


def main():
    """Função principal"""
    print(f"🚀 Iniciando Obelisk Chat + Web Vision...")
    print(f"📡 Ollama URL: {BASE_URL}")
    print(f"🤖 Modelo: {MODEL}")
    print(f"🌐 Selenium: {'✓ Disponível' if SELENIUM_AVAILABLE else '✗ Não instalado'}")
    
    if not SELENIUM_AVAILABLE:
        print("\n⚠️  Para funcionalidades completas de Web Vision:")
        print("   pip install selenium")
    
    root = tk.Tk()
    app = ChatInterface(root)
    
    # Cleanup ao fechar
    def on_closing():
        print("\n🛑 Fechando aplicação...")
        app.browser.close()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
