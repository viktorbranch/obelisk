"""Sistema Inteligente de Processamento de Intenções

Detecta automaticamente a intenção do usuário e executa ações correspondentes.
Funciona com linguagem natural, sem necessidade de comandos específicos.

Exemplos que detecta:
    - "abre o google" → Abre navegador no Google
    - "pesquise python" → Busca "python" no Google  
    - "resumo de notícias" → Acessa sites e extrai manchetes
    - "fecha o chrome" → Fecha navegador
    - "tira um screenshot" → Captura tela

Author: Obelisk AI
License: MIT
"""

import re
from typing import Dict, List, Optional, Tuple


class IntentProcessor:
    """Processador inteligente de intenções do usuário"""
    
    def __init__(self):
        # Mapas de conhecimento do agente
        self.known_sites = {
            'google': 'https://www.google.com',
            'youtube': 'https://www.youtube.com',
            'facebook': 'https://www.facebook.com', 
            'twitter': 'https://www.twitter.com',
            'x': 'https://www.x.com',
            'instagram': 'https://www.instagram.com',
            'linkedin': 'https://www.linkedin.com',
            'github': 'https://www.github.com',
            'gmail': 'https://mail.google.com',
            'whatsapp': 'https://web.whatsapp.com',
            'reddit': 'https://www.reddit.com',
            'amazon': 'https://www.amazon.com.br',
            'mercado livre': 'https://www.mercadolivre.com.br',
            'netflix': 'https://www.netflix.com',
            'wikipedia': 'https://www.wikipedia.org',
            'stackoverflow': 'https://stackoverflow.com',
            'stack overflow': 'https://stackoverflow.com',
            'news': 'https://news.google.com',
            'notícias': 'https://news.google.com',
            'noticias': 'https://news.google.com',
            'g1': 'https://g1.globo.com',
            'uol': 'https://www.uol.com.br',
            'folha': 'https://www.folha.uol.com.br',
            'estadão': 'https://www.estadao.com.br',
            'estadao': 'https://www.estadao.com.br',
            'bbc': 'https://www.bbc.com/portuguese',
            'cnn': 'https://www.cnnbrasil.com.br',
            'yahoo': 'https://www.yahoo.com',
            'bing': 'https://www.bing.com',
            'chatgpt': 'https://chat.openai.com',
            'claude': 'https://claude.ai',
            'gemini': 'https://gemini.google.com',
        }
        
        self.programs = {
            'calculadora': 'calc',
            'calc': 'calc',
            'bloco de notas': 'notepad',
            'notepad': 'notepad',
            'paint': 'mspaint',
            'explorador': 'explorer',
            'explorer': 'explorer',
            'chrome': 'chrome',
            'firefox': 'firefox',
            'edge': 'msedge',
            'word': 'winword',
            'excel': 'excel',
            'powerpoint': 'powerpnt',
            'outlook': 'outlook',
            'cmd': 'cmd',
            'terminal': 'cmd',
            'powershell': 'powershell',
        }
        
        # Padrões de intenção
        self.intent_patterns = {
            'open_site': [
                'abra', 'abre', 'abrir', 'vai no', 'vai na', 'vai para',
                'acessa', 'acessar', 'acesse', 'entra no', 'entra na'
            ],
            'search': [
                'pesquise', 'pesquisa', 'pesquisar', 'busque', 'busca', 'buscar',
                'procure', 'procura', 'procurar', 'google', 'googla'
            ],
            'news': [
                'resumo', 'notícias', 'noticias', 'manchetes', 'headlines',
                'últimas notícias', 'ultimas noticias', 'novidades'
            ],
            'screenshot': [
                'screenshot', 'captura', 'print', 'printar', 'foto da tela',
                'tira um print', 'tira uma foto'
            ],
            'close': [
                'feche', 'fechar', 'fecha', 'encerra', 'encerrar', 'sai do', 'sai da'
            ],
            'execute': [
                'execute', 'executar', 'executa', 'rode', 'rodar', 'roda',
                'inicia', 'iniciar', 'abre', 'abra', 'abrir'
            ]
        }
    
    def detect_intent(self, user_message: str) -> Dict:
        """Detecta a intenção do usuário e retorna ação a executar
        
        Args:
            user_message: Mensagem do usuário em linguagem natural
            
        Returns:
            Dict com: tipo, acao, parametros, confianca
        """
        msg_lower = user_message.lower().strip()
        
        # 1. DETECTA ABERTURA DE SITES
        intent = self._detect_open_site(msg_lower)
        if intent:
            return intent
        
        # 2. DETECTA BUSCA/PESQUISA
        intent = self._detect_search(msg_lower)
        if intent:
            return intent
        
        # 3. DETECTA RESUMO DE NOTÍCIAS
        intent = self._detect_news_summary(msg_lower)
        if intent:
            return intent
        
        # 4. DETECTA SCREENSHOT
        intent = self._detect_screenshot(msg_lower)
        if intent:
            return intent
        
        # 5. DETECTA FECHAR
        intent = self._detect_close(msg_lower)
        if intent:
            return intent
        
        # 6. DETECTA EXECUÇÃO DE PROGRAMA
        intent = self._detect_execute_program(msg_lower)
        if intent:
            return intent
        
        # 7. SEM INTENÇÃO CLARA - conversa normal
        return {
            'tipo': 'conversa',
            'acao': 'CHAT',
            'parametros': {},
            'confianca': 0.3
        }
    
    def _detect_open_site(self, msg: str) -> Optional[Dict]:
        """Detecta se usuário quer abrir algum site"""
        # Verifica se tem palavra de abertura
        has_open_word = any(word in msg for word in self.intent_patterns['open_site'])
        
        # Procura por sites conhecidos
        for site_name, site_url in self.known_sites.items():
            if site_name in msg:
                # Calcula confiança baseada em contexto
                confianca = 0.9 if has_open_word else 0.7
                
                return {
                    'tipo': 'abrir_site',
                    'acao': 'OPEN_BROWSER',
                    'parametros': {
                        'url': site_url,
                        'nome': site_name,
                        'user_message': msg
                    },
                    'confianca': confianca
                }
        
        # Detecta URLs diretas
        url_pattern = r'https?://[^\s]+|www\.[^\s]+|[a-zA-Z0-9-]+\.(com|org|net|br|gov|edu|io|dev|app)[^\s]*'
        urls = re.findall(url_pattern, msg)
        
        if urls and has_open_word:
            url = urls[0]
            if not url.startswith('http'):
                url = 'https://' + url
            
            return {
                'tipo': 'abrir_url',
                'acao': 'OPEN_BROWSER',
                'parametros': {
                    'url': url,
                    'nome': url,
                    'user_message': msg
                },
                'confianca': 0.95
            }
        
        return None
    
    def _detect_search(self, msg: str) -> Optional[Dict]:
        """Detecta se usuário quer fazer uma busca"""
        has_search_word = any(word in msg for word in self.intent_patterns['search'])
        
        if not has_search_word:
            return None
        
        # Extrai termo de busca removendo palavras de comando
        query = msg
        for word in self.intent_patterns['search']:
            query = query.replace(word, '')
        
        # Remove preposições e artigos
        query = re.sub(r'\s+(e|pela|pelo|por|sobre|a|o|os|as|um|uma|pra|para|mim|me|no|na|nos|nas)\s+', ' ', query)
        query = query.strip()
        
        if len(query) < 2:
            return None
        
        return {
            'tipo': 'pesquisa',
            'acao': 'SEARCH',
            'parametros': {
                'query': query,
                'user_message': msg
            },
            'confianca': 0.95
        }
    
    def _detect_news_summary(self, msg: str) -> Optional[Dict]:
        """Detecta se usuário quer resumo de notícias"""
        has_news_word = any(word in msg for word in self.intent_patterns['news'])
        
        if not has_news_word:
            return None
        
        # Determina sites de notícias a acessar
        news_sites = [
            'https://news.google.com',
            'https://g1.globo.com',
            'https://www.bbc.com/portuguese'
        ]
        
        # Se mencionou site específico, adiciona na lista
        for site_name, site_url in self.known_sites.items():
            if site_name in msg and ('notícia' in site_name or 'news' in site_name or site_name in ['g1', 'uol', 'folha', 'cnn', 'bbc']):
                if site_url not in news_sites:
                    news_sites.insert(0, site_url)
        
        return {
            'tipo': 'resumo_noticias',
            'acao': 'NEWS_SUMMARY',
            'parametros': {
                'sites': news_sites,
                'user_message': msg
            },
            'confianca': 0.9
        }
    
    def _detect_screenshot(self, msg: str) -> Optional[Dict]:
        """Detecta se usuário quer screenshot"""
        has_screenshot_word = any(word in msg for word in self.intent_patterns['screenshot'])
        
        if not has_screenshot_word:
            return None
        
        return {
            'tipo': 'screenshot',
            'acao': 'SCREENSHOT',
            'parametros': {
                'user_message': msg
            },
            'confianca': 0.95
        }
    
    def _detect_close(self, msg: str) -> Optional[Dict]:
        """Detecta se usuário quer fechar algo"""
        has_close_word = any(word in msg for word in self.intent_patterns['close'])
        
        if not has_close_word:
            return None
        
        # Detecta o que fechar
        if any(target in msg for target in ['navegador', 'chrome', 'firefox', 'edge', 'browser']):
            return {
                'tipo': 'fechar_navegador',
                'acao': 'CLOSE_BROWSER',
                'parametros': {
                    'user_message': msg
                },
                'confianca': 0.95
            }
        
        if any(target in msg for target in ['aba', 'página', 'pagina', 'site', 'tab']):
            return {
                'tipo': 'fechar_aba',
                'acao': 'CLOSE_TAB',
                'parametros': {
                    'user_message': msg
                },
                'confianca': 0.9
            }
        
        # Padrão: fecha aba atual
        return {
            'tipo': 'fechar',
            'acao': 'CLOSE_TAB',
            'parametros': {
                'user_message': msg
            },
            'confianca': 0.7
        }
    
    def _detect_execute_program(self, msg: str) -> Optional[Dict]:
        """Detecta se usuário quer executar programa"""
        has_execute_word = any(word in msg for word in self.intent_patterns['execute'])
        
        # Procura por programas conhecidos
        for prog_name, prog_cmd in self.programs.items():
            if prog_name in msg:
                confianca = 0.95 if has_execute_word else 0.8
                
                return {
                    'tipo': 'executar_programa',
                    'acao': 'OPEN_APP',
                    'parametros': {
                        'app': prog_cmd,
                        'nome': prog_name,
                        'user_message': msg
                    },
                    'confianca': confianca
                }
        
        return None
    
    def explain_intent(self, intent: Dict) -> str:
        """Gera explicação em português sobre a intenção detectada"""
        tipo = intent['tipo']
        params = intent['parametros']
        
        explanations = {
            'abrir_site': f"Entendi que você quer abrir {params.get('nome', 'um site')}",
            'abrir_url': f"Vou abrir {params.get('url', 'o link')}",
            'pesquisa': f"Vou pesquisar '{params.get('query', '')}' no Google",
            'resumo_noticias': "Vou buscar as principais notícias para você",
            'screenshot': "Vou tirar uma captura de tela",
            'fechar_navegador': "Vou fechar o navegador",
            'fechar_aba': "Vou fechar esta aba",
            'fechar': "Vou fechar",
            'executar_programa': f"Vou abrir {params.get('nome', 'o programa')}",
            'conversa': "Vou processar sua mensagem"
        }
        
        return explanations.get(tipo, "Processando...")


# Exemplo de uso
if __name__ == "__main__":
    processor = IntentProcessor()
    
    # Testes
    test_messages = [
        "abre o google",
        "pesquise python",
        "me dá um resumo das notícias",
        "fecha o chrome",
        "tira um screenshot",
        "abra a calculadora",
        "vai no youtube",
        "busca receitas de bolo",
    ]
    
    print("🧪 Testando detecção de intenções:\n")
    for msg in test_messages:
        intent = processor.detect_intent(msg)
        explanation = processor.explain_intent(intent)
        print(f"📝 '{msg}'")
        print(f"   → {explanation}")
        print(f"   → Ação: {intent['acao']} (confiança: {intent['confianca']:.0%})")
        print()
