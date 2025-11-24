# 🤖 Obelisk AI - Autonomous Computer Agent

**Obelisk** é um agente de IA totalmente autônomo com capacidade de VER, PENSAR e AGIR no seu computador.

![Version](https://img.shields.io/badge/version-3.0.0-blue)
![JavaScript](https://img.shields.io/badge/javascript-ES6+-yellow)
![Electron](https://img.shields.io/badge/electron-28.0.0-brightgreen)
![License](https://img.shields.io/badge/license-MIT-purple)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)

## ✨ Características

### 🎯 Interface Moderna
- **Electron Desktop App**: Interface nativa do Windows
- **Design Neomórfico Dark**: Visual moderno e elegante
- **Animações Suaves**: Experiência fluida e responsiva
- **Sidebar Inteligente**: Acesso rápido a funcionalidades
- **Trigger Bar**: Barra lateral para abrir/fechar rapidamente

### 🧠 IA Conversacional
- **Ollama Integration**: Powered by Llama 3.2
- **Processamento Rápido**: Otimizado para respostas em 2-5s
- **Memória Contextual**: Lembra do histórico da conversa
- **Detecção de Intenções**: Identifica automaticamente o que fazer

### 👁️ **VISÃO COMPUTACIONAL**
- **Captura de Tela em Tempo Real**: Screenshot instantâneo
- **Análise Visual com IA**: Entende e descreve conteúdo visual usando Ollama Vision
- **Detecção de Elementos**: Encontra botões, menus, textos automaticamente
- **Leitura de Texto**: Extrai e lê todo texto visível
- **Guia de Interação**: Instrui onde e como clicar

### 🌐 Automação Web
- **Navegação Inteligente**: Abre sites automaticamente
- **Busca no Google**: Pesquisa e extrai resultados
- **Sites Conhecidos**: 30+ sites pré-configurados
- **Controle Universal**: Funciona com qualquer website

### 🖥️ Controle do Sistema
- **Abertura de Apps**: Calculator, Notepad, Chrome, etc.
- **Comandos de Teclado**: Digita texto e pressiona teclas
- **Automação de Mouse**: Clica em coordenadas específicas
- **Execução Segura**: Roda comandos do sistema

## 🚀 Quick Start

### Requisitos

1. **Node.js 18 ou superior**
   ```bash
   node --version
   npm --version
   ```

2. **Ollama instalado e rodando**
   ```bash
   # Download: https://ollama.ai
   ollama pull llama3.2:latest
   ollama pull llama3.2-vision:latest
   ollama serve
   ```

### Instalação

1. **Clone o repositório**
   ```bash
   git clone https://github.com/yourusername/obelisk.git
   cd obelisk
   ```

2. **Instale as dependências**
   ```bash
   npm install
   ```

3. **Execute o Obelisk**
   ```bash
   npm start
   ```

   Ou use os launchers:
   ```bash
   # Windows
   obelisk.bat           # CMD
   obelisk.vbs           # Modo silencioso
   obelisk_launcher.ps1  # PowerShell
   ```

### Dependências Instaladas

O projeto usa apenas pacotes leves:
- **electron** (28.0.0): Framework desktop
- **axios** (1.6.2): Cliente HTTP para Ollama
- **screenshot-desktop** (^1.15.0): Captura de tela
- **sharp** (^0.33.0): Processamento de imagem

Total: ~4 pacotes principais (sem compilação nativa complexa)

## 📖 Uso

## 📖 Uso

### Comandos de Visão
```
"O que você vê na tela?"
"Encontre o botão de login"
"Leia o texto da tela"
"Descreva o que está aparecendo"
"Onde devo clicar para salvar?"
```

### Navegação Web
```
"Abra o YouTube"
"Pesquise por tutoriais de JavaScript"
"Entre no GitHub"
```

### Controle do Sistema
```
"Abra a calculadora"
"Abra o bloco de notas"
"Tire um screenshot"
```

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────┐
│         Electron Desktop App                │
├─────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌───────────┐ │
│  │  Trigger │  │   Chat   │  │  Sidebar  │ │
│  │   Bar    │  │  Window  │  │  Controls │ │
│  └──────────┘  └──────────┘  └───────────┘ │
├─────────────────────────────────────────────┤
│              Main Process (Node.js)         │
│  ┌──────────────┐      ┌─────────────────┐ │
│  │   Ollama     │◄────►│  Agent Engine   │ │
│  │   API        │      │  (Intent + AI)  │ │
│  └──────────────┘      └─────────────────┘ │
│         ▲                      ▲            │
│         │                      │            │
│         ▼                      ▼            │
│  ┌──────────────┐      ┌─────────────────┐ │
│  │   Vision     │      │   System        │ │
│  │   Module     │      │   Automation    │ │
│  └──────────────┘      └─────────────────┘ │
└─────────────────────────────────────────────┘
```

### Componentes Principais

1. **scripts/main.js**: Processo principal do Electron, gerencia janelas
2. **scripts/agent.js**: Engine de IA, detecção de intenções, automação
3. **scripts/vision.js**: Módulo de visão computacional com Ollama Vision
4. **index.html**: Interface do chat
5. **css/**: Estilos neomórficos dark theme

### Fluxo de Execução

1. Usuário digita mensagem no chat
2. `agent.js` detecta a intenção (OPEN_BROWSER, SEARCH, etc.)
3. Se precisar de visão, chama `vision.js`
4. Executa ação (abre site, busca, captura tela, etc.)
5. Retorna resposta ao chat

## 🎨 Personalização

### Alterar Modelo Ollama

Edite `scripts/main.js`:
```javascript
const MODEL = 'llama3.2:latest'; // Trocar modelo de chat
```

Edite `scripts/vision.js`:
```javascript
const VISION_MODEL = 'llama3.2-vision:latest'; // Trocar modelo de visão
```

### Ajustar Timeout

Edite `scripts/agent.js`:
```javascript
timeout: 30000, // 30 segundos
num_predict: 50, // Tokens máximos
```

### Adicionar Sites Conhecidos

Edite `scripts/agent.js`:
```javascript
const KNOWN_SITES = {
    'meusite': 'https://meusite.com',
    // ...
};
```
4. **ChatInterface**: User interface and interaction

## 🎮 Operating Modes

### Normal Mode
- Interactive chat with Ollama
- Manual web commands
- Step-by-step assistance

### Autonomous Mode (🤖)
- **Fully automatic** task execution
- **Self-directed** planning and action
- **No confirmation** required
- **Real-time** progress updates

## 🛠️ Configuration

### Environment Variables

```bash
# Ollama Configuration
export OLLAMA_URL=http://127.0.0.1:11434
export OLLAMA_MODEL=llama3.2:latest

# Agent Configuration
export OBELISK_MAX_ITERATIONS=20
export OBELISK_DELAY=2
```

### Customization

Edit `examples/ollama_chat_web.py`:

```python
# Maximum task iterations
self.max_iterations = 20

# Delay between actions (seconds)
time.sleep(2)

# Analysis timeout (seconds)
timeout=30
```

## 📊 Performance

- **Startup Time**: 2-3 seconds
- **Action Execution**: 0.5-1 second
- **LLM Analysis**: 1-5 seconds
- **Web Page Load**: 2-3 seconds
- **Screenshot Capture**: 0.1 seconds

## 🔒 Security & Privacy

### ⚠️ Important Warnings

- **Full System Access**: Obelisk can control your entire computer
- **Autonomous Actions**: Executes without confirmation in autonomous mode
- **Screen Capture**: May capture sensitive information
- **Network Access**: Makes web requests and downloads content

### Best Practices

✅ **Recommended**
- Use in controlled test environments
- Review tasks before enabling autonomous mode
- Monitor execution in real-time
- Keep antivirus active

❌ **Not Recommended**
- Production environments
- Financial transactions
- Access to sensitive accounts
- Unattended operation with critical data

## 🧪 Development

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black examples/
```

### Adding Features

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests
5. Submit a pull request

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Roadmap

- [ ] Multi-language support
- [ ] OCR integration for text recognition
- [ ] Voice command interface
- [ ] Cloud model support (GPT-4, Claude)
- [ ] Task templates and macros
- [ ] Multi-monitor support
- [ ] Mobile device control
- [ ] API for external integrations

## 📚 Documentation

- [User Guide](examples/CHAT_WEB_CONTROL.md) - Complete feature documentation
- [Autonomous Agent Guide](examples/AGENTE_AUTONOMO.md) - Autonomous mode details
- [API Reference](docs/API.md) - Developer documentation

## 🙏 Acknowledgments

Built with:
- **Ollama** - Local LLM inference
- **Selenium** - Web browser automation
- **PyAutoGUI** - System control
- **BeautifulSoup** - HTML parsing
- **Tkinter** - GUI framework

## 💡 Support

- **Issues**: [GitHub Issues](https://github.com/obelisk-ai/obelisk/issues)
- **Discussions**: [GitHub Discussions](https://github.com/obelisk-ai/obelisk/discussions)
- **Email**: contact@obelisk-ai.dev

## 🌟 Star History

If you find Obelisk useful, please consider giving it a star! ⭐

---

**Made with ❤️ by the Obelisk AI Team**

*Autonomous intelligence for everyone*
