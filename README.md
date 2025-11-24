# 🤖 Obelisk AI - Autonomous Computer Agent

**Obelisk** is a fully autonomous AI agent powered by Ollama that can see, think, and act on your computer with complete independence.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8%2B-green)
![License](https://img.shields.io/badge/license-MIT-purple)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

## ✨ Features

### 🎯 Autonomous Operation
- **Zero Supervision**: Plans and executes tasks from start to finish
- **Adaptive Intelligence**: Adjusts actions based on real-time feedback
- **Multi-Step Planning**: Breaks down complex tasks into actionable steps
- **Self-Correction**: Learns from errors and adapts strategy

### 👁️ Computer Vision
- **Screen Monitoring**: Continuous screenshot capture
- **Visual Analysis**: Understands screen content and context
- **Element Detection**: Identifies buttons, links, and UI components
- **Real-Time Awareness**: Tracks mouse position and active windows

### 🌐 Web Automation
- **Smart Navigation**: Opens URLs and navigates sites automatically
- **Intelligent Search**: Performs Google searches with natural language
- **Content Extraction**: Parses HTML and extracts relevant information
- **Interactive Elements**: Clicks buttons, fills forms, scrolls pages
- **Universal Compatibility**: Works with any website

### 🖥️ System Control
- **Application Launcher**: Opens programs (Calculator, Notepad, etc.)
- **Keyboard Control**: Types text and presses keys
- **Mouse Automation**: Clicks at specific coordinates
- **Screenshot Capture**: Takes and saves screen captures
- **Command Execution**: Runs system commands safely

### 💬 Natural Language Interface
- **Conversational AI**: Chat naturally with Ollama LLM
- **Intent Detection**: Understands what you want to accomplish
- **Context Awareness**: Remembers conversation history
- **Proactive Suggestions**: Recommends next steps

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8 or higher**
   ```bash
   python --version
   ```

2. **Ollama installed and running**
   ```bash
   # Download from https://ollama.ai
   ollama pull llama3.2
   ollama serve
   ```

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/obelisk-ai/obelisk.git
   cd obelisk
   ```

2. **Install dependencies** (only 6 packages!)
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Obelisk**
   ```bash
   # Windows (recommended)
   scripts\start_obelisk_chat.bat

   # Direct Python execution
   python src/obelisk_agent.py
   
   # Or as module
   python -m src.obelisk_agent

   # Linux/macOS
   python3 src/obelisk_agent.py
   ```

4. **Optional: Create desktop shortcut** (Windows)
   ```powershell
   powershell -ExecutionPolicy Bypass -File scripts/create_shortcut.ps1
   ```

## 📖 Usage Examples

### Web Research
```
"Search for GOTY 2024 winners and tell me who won"
"Find Python tutorials on YouTube"
"Get the latest news about artificial intelligence"
```

### System Automation
```
"Open calculator and compute 1234 * 5678"
"Create a note in Notepad with my task list"
"Take a screenshot and save it"
```

### Complex Tasks
```
"Research the top 5 programming languages and create a comparison"
"Find recipes for chocolate cake and save the best one"
"Check my calendar and remind me of today's events"
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│            User Interface (Tkinter)         │
├─────────────────────────────────────────────┤
│                                             │
│  ┌──────────────┐      ┌─────────────────┐ │
│  │   Ollama     │◄────►│  Autonomous     │ │
│  │   Chat       │      │  Agent Engine   │ │
│  └──────────────┘      └─────────────────┘ │
│         ▲                      ▲            │
│         │                      │            │
│         ▼                      ▼            │
│  ┌──────────────┐      ┌─────────────────┐ │
│  │   Browser    │      │   System        │ │
│  │   Controller │      │   Controller    │ │
│  └──────────────┘      └─────────────────┘ │
│         │                      │            │
└─────────┼──────────────────────┼────────────┘
          ▼                      ▼
    ┌──────────┐          ┌──────────┐
    │ Selenium │          │PyAutoGUI │
    │   Web    │          │  System  │
    └──────────┘          └──────────┘
```

### Core Components

1. **AutonomousAgent**: Vision, planning, and execution loop
2. **OllamaChat**: LLM communication and context management
3. **BrowserController**: Web automation with Selenium
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
