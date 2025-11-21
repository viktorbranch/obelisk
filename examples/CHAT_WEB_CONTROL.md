# Obelisk Chat + Web Vision + PC Control 🚀

Interface gráfica para conversar com Ollama com capacidade de **ver, interagir e controlar** páginas web e seu PC em tempo real.

## 🌟 Características

### 💬 Chat & IA
- Chat interativo com Ollama (llama3.2:latest)
- Contexto automático: cada mensagem recebe conteúdo da página aberta
- Memória de conversação inteligente
- Interface moderna e responsiva

### 🌐 Web Automation
- **Navegação web** automatizada com Selenium
- 👁️ **Visão real** de páginas web (não apenas links!)
- 🎯 **Análise inteligente** de HTML com BeautifulSoup
- 🔍 **Filtros avançados** para extrair conteúdo relevante
- 🖱️ **Clique em elementos** por texto natural
- 🌍 Funciona em **qualquer website** automaticamente
- 📱 Detecção natural de sites comuns (google, youtube, github, etc)
- ❌ **Fechar abas e navegador** por comando
- 📜 Scroll automático e navegação inteligente

### 🖥️ PC Control (NOVO!)
- 📸 **Captura de tela** (screenshots)
- ⌨️ **Controle de teclado** (digitar texto, pressionar teclas)
- 🖱️ **Controle de mouse** (cliques, movimentos)
- 🚀 **Executar programas** (calculadora, notepad, paint, etc)
- 🎮 **Controle total** do sistema via PyAutoGUI
- 💻 **Comandos do sistema** Windows/Linux/Mac

## 🚀 Instalação Rápida

### 1. Pré-requisitos

```bash
# Python 3.8+
python --version

# Ollama instalado e rodando
ollama --version
ollama list  # Verifica modelos instalados
```

Se não tiver o Ollama:
1. Baixe em https://ollama.ai
2. Instale o modelo: `ollama pull llama3.2`

### 2. Instalar dependências

```bash
# Todas as dependências necessárias
pip install selenium beautifulsoup4 requests pyautogui
```

### 3. Executar

```bash
# Windows - Usando o script de atalho
start_obelisk_chat.bat

# Ou diretamente em qualquer OS
python examples/ollama_chat_web.py
```

### 4. Criar atalho na área de trabalho (Windows)

```powershell
powershell -ExecutionPolicy Bypass -File create_shortcut.ps1
```

Agora você tem um atalho **Obelisk Chat** na sua área de trabalho!

## 📖 Exemplos de Uso

### 🌐 Navegação Web

**Linguagem natural - sites comuns:**
```
Usuário: abre o google
Usuário: abre o youtube
Usuário: abre o github
Usuário: visite o reddit
```

**URLs específicas:**
```
Usuário: abre https://news.google.com
Usuário: acesse www.wikipedia.org
Usuário: vá para github.com/usuario/repo
```

**Notícias e conteúdo:**
```
Usuário: abre google notícias e me diz a primeira manchete
Usuário: qual a primeira notícia?
Usuário: resuma essa página para mim
```

### 🖱️ Interação com Páginas

**Clicar em elementos:**
```
Usuário: clique em "Login"
Usuário: clica no botão "Próximo"
Usuário: aperte "Pesquisar"
```

**Ver elementos disponíveis:**
```
Usuário: quais botões posso clicar?
Usuário: me mostre os elementos da página
Usuário: o que tem disponível aqui?
```

**Navegação:**
```
Usuário: rola a página pra baixo
Usuário: volte ao topo
Usuário: vai pro final da página
```

### ❌ Fechar e Gerenciar

**Fechar navegador:**
```
Usuário: fecha o navegador
Usuário: fecha o chrome
Usuário: sai do navegador
```

**Fechar abas:**
```
Usuário: fecha essa aba
Usuário: fecha a página
Usuário: fecha o google
```

### 🖥️ Controle do PC

**Screenshots:**
```
Usuário: tira um screenshot
Usuário: tire print da tela
Usuário: captura a tela
```

**Executar programas:**
```
Usuário: abre o bloco de notas
Usuário: abra a calculadora
Usuário: execute o paint
Usuário: abre o explorador de arquivos
```

**Comandos de teclado:**
```
Usuário: pressione Enter
Usuário: aperte Esc
Usuário: digite "Olá mundo"
```

### 💬 Conversação com Contexto

O assistente **sempre vê** a página aberta:

```
Usuário: abre google notícias
Assistente: [Abre e analisa automaticamente]
          Abri o Google Notícias! Estou vendo 15 manchetes...
          A primeira notícia é: "..."

Usuário: me fale mais sobre a terceira
Assistente: [Analisa a terceira manchete automaticamente]
          A terceira manchete fala sobre...

Usuário: clica nela
Assistente: [Clica e analisa nova página]
          Cliquei! Agora estou na página do artigo...
```

**Não precisa repetir comandos!** O assistente mantém contexto da página aberta.

## 🎨 Interface

### Janela Principal

```
┌─────────────────────────────────────────────┐
│ Obelisk - Chat com Ollama + Web            │
├─────────────────────────────────────────────┤
│                                             │
│  [Área de Chat com histórico]              │
│                                             │
│  Usuário: abre o google                    │
│  Sistema: 🌐 Abrindo Google...             │
│  Assistente: Abri o Google! Estou vendo... │
│                                             │
├─────────────────────────────────────────────┤
│  [Digite sua mensagem...]                  │
│                           [Enviar] [Limpar] │
└─────────────────────────────────────────────┘
```

### Atalhos de Teclado

- **Enter**: Envia mensagem
- **Shift+Enter**: Nova linha na mensagem
- **Ctrl+L**: Limpa chat

### Mensagens do Sistema

- 🔄 Iniciando navegador...
- 🌐 Abrindo [site]...
- 🔍 Analisando página...
- 🖱️ Clicando em...
- 🔴 Fechando navegador...
- 📸 Tirando screenshot...
- 🚀 Abrindo programa...
- ✓ Operação concluída
- ✗ Erro ao executar

## 🛠️ Comandos Avançados

### Comandos do Sistema

```bash
/clear      # Limpa o chat
/reset      # Reinicia conversa com Ollama
/browser    # Status do navegador
/help       # Ajuda (lista comandos)
```

### Configuração de Ambiente

```bash
# Windows
set OLLAMA_URL=http://127.0.0.1:11434
set OLLAMA_MODEL=llama3.2:latest

# Linux/Mac
export OLLAMA_URL=http://127.0.0.1:11434
export OLLAMA_MODEL=llama3.2:latest
```

## 🔧 Arquitetura

### Classes Principais

1. **OllamaChat** (`examples/ollama_chat_web.py`)
   - Gerencia comunicação com Ollama
   - Mantém histórico de conversação
   - Injeta contexto automaticamente

2. **BrowserController** (`examples/ollama_chat_web.py`)
   - Controla Selenium WebDriver
   - Analisa páginas com BeautifulSoup
   - Extrai conteúdo relevante
   - Gerencia cliques e interações
   - **Controla sistema com PyAutoGUI**
   - **Executa comandos do sistema**

3. **ChatInterface** (`examples/ollama_chat_web.py`)
   - Interface gráfica Tkinter
   - Processa comandos e ações
   - Detecta intenções automaticamente
   - Gerencia threads para não travar

### Fluxo de Processamento

```
Usuário digita mensagem
        ↓
Interface detecta intenção
        ↓
┌───────┴────────┐
│                │
Web Action?   Sistema?
│                │
↓                ↓
Selenium     PyAutoGUI
+ BS4        + subprocess
│                │
└───────┬────────┘
        ↓
Contexto gerado
        ↓
Enviado ao Ollama
        ↓
Resposta com contexto
        ↓
Exibido ao usuário
```

### Detecção Automática

O sistema detecta automaticamente:

1. **Sites comuns**: google, youtube, facebook, github, etc
2. **URLs**: http://, https://, www.
3. **Comandos de fechar**: fecha, feche, sai
4. **Comandos de interação**: clique, aperte, pressione
5. **Comandos de sistema**: screenshot, print, abre programa
6. **Análise**: analise, resuma, me fale sobre

## 🎯 Casos de Uso

### 1. Pesquisa e Análise Web
```
"Abre google notícias e me resume as principais manchetes de hoje"
"Acesse wikipedia.org/Python e me explique o que é"
"Vai no github.com/microsoft/vscode e me diz do que se trata"
```

### 2. Automação de Tarefas
```
"Abre google.com, pesquisa por 'Python tutorials' e clica no primeiro resultado"
"Vai no youtube e me mostra os vídeos em destaque"
"Acessa meu email e me diz se tenho mensagens novas"
```

### 3. Produtividade
```
"Tira um screenshot da página atual"
"Abre o bloco de notas e anota isso: [texto]"
"Abre a calculadora"
```

### 4. Assistente Pessoal
```
"O que tem de novo nas notícias?"
"Me ajuda a pesquisar sobre [assunto]"
"Fecha todas as abas e me ajuda com outra coisa"
```

## 🐛 Troubleshooting

### Ollama não responde

```bash
# Verificar se Ollama está rodando
ollama list

# Iniciar Ollama manualmente (se necessário)
ollama serve

# Testar conexão
curl http://127.0.0.1:11434/api/tags
```

### Chrome não abre

```bash
# Reinstalar Selenium
pip install --upgrade selenium

# Verificar ChromeDriver
# O Selenium baixa automaticamente, mas você pode instalar manualmente
```

### PyAutoGUI não funciona

```bash
# Reinstalar PyAutoGUI
pip install --upgrade pyautogui

# No Linux, pode precisar de:
sudo apt-get install python3-tk python3-dev
```

### Erro de "InvalidSessionId"

Isso acontece quando o navegador é fechado manualmente. O sistema detecta e reinicia automaticamente.

## 📊 Performance

- **Inicialização**: ~2-3 segundos (incluindo Chrome)
- **Análise de página**: ~1-2 segundos
- **Resposta do Ollama**: ~1-5 segundos (depende do modelo)
- **Clique em elemento**: ~0.5 segundos
- **Screenshot**: ~0.1 segundos

## 🔒 Segurança

⚠️ **IMPORTANTE**: Este sistema tem controle total do seu PC!

- **Comandos de sistema**: Use com cuidado
- **Execução de programas**: Apenas programas confiáveis
- **Screenshots**: Podem capturar informações sensíveis
- **Navegação web**: Sempre verifique URLs antes de abrir

### Recomendações:
1. Não execute em ambiente de produção
2. Revise código antes de rodar comandos sensíveis
3. Use em ambiente controlado para testes
4. Mantenha antivírus ativo

## 📝 Logs e Debug

O sistema imprime logs no terminal:

```
🚀 Iniciando Obelisk Chat + Web Vision...
📡 Ollama URL: http://127.0.0.1:11434
🤖 Modelo: llama3.2:latest
🌐 Selenium: ✓ Disponível
✓ Driver do Chrome inicializado
✓ Navegando para: https://news.google.com
✓ Manchetes extraídas: 15 manchetes
✓ Texto clicado: "Login"
✓ Screenshot salvo: screenshot_20240101_120000.png
```

## 🎓 Aprendizado e Evolução

Este projeto começou como um simples chat com Ollama e evoluiu para:

1. ✅ Chat básico com Ollama
2. ✅ Navegação web com Selenium
3. ✅ Visão real de páginas (BeautifulSoup)
4. ✅ Interação com elementos
5. ✅ Detecção de linguagem natural
6. ✅ Contexto automático
7. ✅ Controle total do PC (PyAutoGUI)
8. ✅ Fechar navegador/abas
9. 🔄 Em desenvolvimento: File system, mais automações

## 🤝 Contribuindo

Ideias para melhorias:

- [ ] Suporte a múltiplas abas simultâneas
- [ ] Histórico de navegação
- [ ] Bookmarks automáticos
- [ ] Integração com mais navegadores
- [ ] OCR de imagens na página
- [ ] Gravação de macros
- [ ] Automação de formulários
- [ ] Download de arquivos
- [ ] Upload de arquivos
- [ ] Geração de relatórios

## 📄 Licença

Parte do projeto Obelisk - Veja LICENSE para detalhes

## 🙏 Créditos

- **Selenium**: Automação web
- **BeautifulSoup**: Parse de HTML
- **PyAutoGUI**: Controle de sistema
- **Ollama**: LLM local
- **Tkinter**: Interface gráfica

---

**Desenvolvido com ❤️ para automação inteligente**

*"Do chat ao controle total do PC - sua IA pessoal sem limites"*
