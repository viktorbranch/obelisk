# Contributing to Obelisk AI

Thank you for your interest in contributing to Obelisk! This document provides guidelines for contributing to the project.

## 🎯 How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/obelisk-ai/obelisk/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version, Ollama version)
   - Screenshots if applicable

### Suggesting Features

1. Check [Discussions](https://github.com/obelisk-ai/obelisk/discussions) for similar ideas
2. Create a new discussion describing:
   - The feature and its benefits
   - Use cases
   - Potential implementation approach

### Pull Requests

1. **Fork** the repository
2. **Create** a branch: `git checkout -b feature/your-feature-name`
3. **Make** your changes
4. **Test** thoroughly
5. **Commit** with clear messages
6. **Push** to your fork
7. **Open** a Pull Request

## 📝 Development Guidelines

### Code Style

- Follow **PEP 8** conventions
- Use **black** for code formatting: `black examples/`
- Add **docstrings** to functions and classes
- Keep functions **focused** and **small**

### Testing

- Add tests for new features
- Run existing tests: `pytest tests/`
- Ensure all tests pass before submitting PR

### Documentation

- Update README.md if adding features
- Add inline comments for complex logic
- Update relevant .md files in `examples/`

## 🏗️ Project Structure

```
obelisk/
├── examples/
│   ├── ollama_chat_web.py       # Main application
│   ├── AGENTE_AUTONOMO.md       # Autonomous mode docs
│   └── CHAT_WEB_CONTROL.md      # Feature documentation
├── tests/
│   └── test_*.py                # Test files
├── requirements.txt             # Dependencies
├── setup.py                     # Package setup
└── README.md                    # Main documentation
```

## 🔍 Areas for Contribution

### High Priority

- [ ] Multi-language support
- [ ] Improved error handling
- [ ] Performance optimizations
- [ ] Cross-platform testing

### Medium Priority

- [ ] OCR integration
- [ ] Voice commands
- [ ] Cloud LLM support
- [ ] Task templates

### Nice to Have

- [ ] Mobile device control
- [ ] Multi-monitor support
- [ ] Recording/replay macros
- [ ] API for integrations

## ✅ Checklist Before Submitting

- [ ] Code follows project style
- [ ] Tests added and passing
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] No merge conflicts
- [ ] Feature works on Windows/Linux/macOS (if applicable)

## 🤝 Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what's best for the project
- Help newcomers get started

## 📧 Contact

- **Issues**: Technical problems and bugs
- **Discussions**: Feature ideas and questions
- **Email**: contact@obelisk-ai.dev

Thank you for contributing to Obelisk AI! 🚀
