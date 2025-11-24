# 📦 Source Code - Obelisk AI

Este diretório contém todo o código fonte do Obelisk AI.

## 📁 Estrutura

```
src/
├── __init__.py              # Inicialização do pacote
├── obelisk_agent.py         # Aplicação principal (2,502 linhas)
├── config.py                # Configurações centralizadas
│
├── core/                    # Módulos principais
│   ├── __init__.py
│   └── intent_processor.py  # Processador de intenções (384 linhas)
│
└── utils/                   # Utilitários
    └── __init__.py
```

## 🎯 Módulos Principais

### `obelisk_agent.py`
**Aplicação principal completa** com:
- `OllamaChat` - Cliente de comunicação com Ollama
- `AutonomousAgent` - Agente autônomo com visão e planejamento
- `BrowserController` - Controle de navegador web com Selenium
- `ChatInterface` - Interface gráfica Tkinter

**Uso**:
```bash
python src/obelisk_agent.py
# ou
python -m src.obelisk_agent
```

### `config.py`
**Configurações centralizadas** para:
- Ollama (URL, modelo)
- Agente (iterações, delays)
- Navegador (headless, timeout)
- UI (tamanho, tema)
- Logging (nível, arquivo)

**Edite este arquivo para customizar o comportamento!**

### `core/intent_processor.py`
**Processador inteligente de intenções** que:
- Detecta intenção do usuário (95%+ precisão)
- Mapeia 30+ sites conhecidos
- Reconhece 15+ programas
- Gera ações automáticas

**Exemplo**:
```python
from src.core.intent_processor import IntentProcessor

processor = IntentProcessor()
intent = processor.detect_intent("abre o google")
# → {'tipo': 'abrir_site', 'acao': 'OPEN_BROWSER', ...}
```

## 🚀 Como Executar

### Método 1: Script de inicialização
```bash
scripts\start_obelisk_chat.bat
```

### Método 2: Python direto
```bash
python src\obelisk_agent.py
```

### Método 3: Como módulo
```bash
python -m src.obelisk_agent
```

### Método 4: Instalado (após `pip install -e .`)
```bash
obelisk
```

## 🔧 Desenvolvimento

### Adicionar Novo Módulo Core
```bash
# 1. Crie o arquivo em src/core/
src/core/novo_modulo.py

# 2. Adicione ao __init__.py
# src/core/__init__.py
from .novo_modulo import MinhaClasse
__all__ = ['IntentProcessor', 'MinhaClasse']

# 3. Use no código principal
from src.core import MinhaClasse
```

### Adicionar Utilitário
```bash
# 1. Crie em src/utils/
src/utils/helper.py

# 2. Adicione ao __init__.py
# src/utils/__init__.py
from .helper import funcao_util
__all__ = ['funcao_util']
```

## 📊 Estatísticas de Código

| Arquivo | Linhas | Descrição |
|---------|--------|-----------|
| `obelisk_agent.py` | 2,502 | App principal completo |
| `intent_processor.py` | 384 | Detecção de intenções |
| `config.py` | 30 | Configurações |
| `__init__.py` (src) | 15 | Inicialização pacote |
| `__init__.py` (core) | 7 | Inicialização core |
| `__init__.py` (utils) | 5 | Inicialização utils |
| **TOTAL** | **2,943** | **Linhas de código** |

## 🧪 Testes

```bash
# Testar intent processor isoladamente
python src/core/intent_processor.py

# Testar aplicação completa
python src/obelisk_agent.py
```

## 📦 Instalação como Pacote

```bash
# Modo desenvolvimento (edições refletem imediatamente)
pip install -e .

# Modo produção
pip install .

# Depois pode usar de qualquer lugar:
obelisk
```

## 🔗 Imports Recomendados

### Import Absoluto (Recomendado)
```python
from src.core.intent_processor import IntentProcessor
from src.config import OLLAMA_URL
```

### Import Relativo (Dentro do pacote)
```python
from .core.intent_processor import IntentProcessor
from .config import OLLAMA_URL
```

### Import com Fallback (Mais robusto)
```python
try:
    from src.core.intent_processor import IntentProcessor
except ImportError:
    from core.intent_processor import IntentProcessor
```

## 🎯 Próximos Passos

### v1.1 - Modularização Completa
- [ ] Separar `BrowserController` em arquivo próprio
- [ ] Separar `AutonomousAgent` em arquivo próprio
- [ ] Separar `OllamaChat` em arquivo próprio
- [ ] Separar `ChatInterface` para `src/ui/`

### v1.2 - Testes
- [ ] Criar `tests/` na raiz
- [ ] Testes unitários para cada módulo
- [ ] Testes de integração
- [ ] CI/CD com GitHub Actions

### v1.3 - Recursos Avançados
- [ ] Logger estruturado em `src/utils/logger.py`
- [ ] Validadores em `src/utils/validators.py`
- [ ] Cache de resultados
- [ ] Histórico persistente

## 📚 Documentação Completa

Veja a pasta `docs/` para documentação detalhada:
- `docs/AGENTE_AUTONOMO.md` - Modo autônomo
- `docs/INTENT_DETECTION.md` - Sistema de intenções
- `docs/CAPTCHA_SOLUTION.md` - Anti-reCAPTCHA
- `docs/NEW_STRUCTURE.md` - Esta estrutura

---

**Estrutura criada em**: 24/11/2025  
**Versão**: 1.0.0  
**Licença**: MIT
