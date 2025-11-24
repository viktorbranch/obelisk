# 🤖 Obelisk - Agente Autônomo AI

## Visão Geral

O **Agente Autônomo** é um sistema de IA que pode **ver, planejar e executar** tarefas no seu computador de forma completamente independente.

## 🎯 Características Principais

### 1. **Visão da Tela** 👁️
- Captura screenshots continuamente
- Monitora posição do mouse e janelas ativas
- Analisa o estado atual do sistema

### 2. **Planejamento Inteligente** 🧠
- Usa Ollama LLM para determinar próximos passos
- Adapta o plano conforme resultados
- Estima progresso da tarefa (0-100%)

### 3. **Execução Autônoma** ⚡
- Clica em posições específicas
- Digita texto automaticamente
- Abre programas e aplicações
- Realiza buscas no Google
- Pressiona teclas do sistema
- Aguarda quando necessário

### 4. **Loop Adaptativo** 🔄
```
┌─────────────────────────────────────┐
│  1. CAPTURA TELA                    │
│     ↓                                │
│  2. ANALISA SITUAÇÃO (Ollama)       │
│     ↓                                │
│  3. DETERMINA PRÓXIMO PASSO         │
│     ↓                                │
│  4. EXECUTA AÇÃO                    │
│     ↓                                │
│  5. VERIFICA RESULTADO              │
│     ↓                                │
│  └──→ Repete até concluir           │
└─────────────────────────────────────┘
```

## 🚀 Como Usar

### 1. **Ativar Modo Autônomo**

1. Abra o Obelisk Chat
2. Clique no botão **"🤖 Modo Autônomo"**
3. O botão ficará vermelho: **"🤖 MODO ATIVO"**

### 2. **Dar uma Tarefa**

Digite uma tarefa completa e pressione Enter:

```
"Pesquise pela votação do GOTY e me diga quem ganhou"
```

### 3. **Observar Execução**

O agente irá:
1. 🔍 Capturar a tela
2. 🧠 Analisar a situação
3. 📊 Mostrar progresso (%)
4. 👁️ Reportar o que está vendo
5. ▶️ Informar próximo passo
6. ⚡ Executar ação
7. 🔄 Repetir até completar

### 4. **Receber Resultado**

Quando concluído, o agente:
- ✅ Marca como TAREFA COMPLETA
- 📊 Mostra total de passos executados
- 💬 Gera resumo do que foi feito

## 📖 Exemplos de Tarefas

### Pesquisa Web
```
"Pesquise pela votação do GOTY 2024"
"Busque notícias sobre inteligência artificial"
"Procure receitas de bolo de chocolate"
```

**O agente vai:**
1. Detectar que precisa buscar
2. Abrir Google automaticamente
3. Digitar o termo de busca
4. Pressionar Enter
5. Analisar resultados
6. Reportar o que encontrou

### Abrir Aplicações
```
"Abra a calculadora e calcule 123 * 456"
"Abra o bloco de notas e escreva minha lista de tarefas"
"Execute o Paint"
```

**O agente vai:**
1. Detectar programa necessário
2. Abrir via Win+R
3. Digitar comandos (se necessário)
4. Executar a tarefa solicitada

### Captura e Documentação
```
"Tire prints da tela a cada 10 segundos"
"Capture a tela e salve com timestamp"
"Documente o que está na tela"
```

### Navegação Complexa
```
"Abra o YouTube e encontre vídeos sobre Python"
"Vá no GitHub e mostre repositórios populares"
"Acesse meu email e me diga se tenho mensagens novas"
```

## ⚙️ Ações Disponíveis

O agente pode executar estas ações:

| Ação | Descrição | Parâmetros |
|------|-----------|------------|
| **SEARCH** | Busca no Google | `{"query": "termo"}` |
| **OPEN_APP** | Abre programa | `{"app": "calc"}` |
| **TYPE** | Digita texto | `{"texto": "conteúdo"}` |
| **PRESS_KEY** | Pressiona tecla | `{"key": "enter"}` |
| **CLICK** | Clica em posição | `{"x": 100, "y": 200}` |
| **WAIT** | Aguarda | `{"segundos": 2}` |
| **DONE** | Tarefa completa | - |

## 🎛️ Configurações

### Máximo de Iterações
Por padrão, o agente executa até **20 iterações** por tarefa.

Para ajustar, modifique em `AutonomousAgent.__init__`:
```python
self.max_iterations = 20  # Altere para mais ou menos
```

### Delay Entre Ações
Padrão: **2 segundos** entre cada iteração.

Para ajustar, modifique em `run_autonomous_task`:
```python
time.sleep(2)  # Altere o valor
```

### Timeout do Ollama
Padrão: **30 segundos** por análise.

Para ajustar, modifique em `analyze_screen_with_vision`:
```python
timeout=30  # Altere o valor
```

## 🔍 Como Funciona Internamente

### Classe AutonomousAgent

```python
class AutonomousAgent:
    def __init__(self, base_url, model):
        self.current_task = None
        self.task_steps = []
        self.completed_steps = []
        self.max_iterations = 20
    
    def capture_screen(self):
        # Captura screenshot
        
    def analyze_screen_with_vision(self, task, screen):
        # Analisa com Ollama e determina próximo passo
        
    def execute_action(self, action_data):
        # Executa a ação determinada
        
    def run_autonomous_task(self, task, progress_callback):
        # Loop principal: captura → analisa → executa
```

### Fluxo de Decisão

O agente usa **palavras-chave** para detectar intenção:

```python
# Busca no Google
if "pesquise" in task or "busque" in task:
    return {"acao": "SEARCH", ...}

# Abrir programa  
if "abra" in task or "execute" in task:
    return {"acao": "OPEN_APP", ...}
```

### Análise com Ollama

O agente envia este prompt para o Ollama:

```
TAREFA DO USUÁRIO: {task}

INFORMAÇÕES DA TELA:
- Mouse: (x, y)
- Tela: (width, height)

Determine o próximo passo em JSON:
{
  "observacao": "...",
  "proximo_passo": "...",
  "acao": "SEARCH|OPEN_APP|...",
  "parametros": {...},
  "progresso": 0-100
}
```

## 📊 Exemplo de Execução

**Tarefa:** "Pesquise pela votação do GOTY"

```
🎯 INICIANDO TAREFA AUTÔNOMA: Pesquise pela votação do GOTY
══════════════════════════════════════════════════════════

🔍 Iteração 1: Capturando tela...
🧠 Analisando situação atual...
📊 Progresso: 20%
👁️ Vejo: Detectada necessidade de buscar: votação do GOTY
▶️ Próximo passo: Buscar 'votação do GOTY' no Google
⚡ Executando: SEARCH
✓ Busca iniciada: votação do GOTY

🔍 Iteração 2: Capturando tela...
🧠 Analisando situação atual...
📊 Progresso: 60%
👁️ Vejo: Página de resultados do Google
▶️ Próximo passo: Analisar resultados da busca
⚡ Executando: WAIT

🔍 Iteração 3: Capturando tela...
🧠 Analisando situação atual...
📊 Progresso: 100%
▶️ Próximo passo: Tarefa concluída
⚡ Executando: DONE

══════════════════════════════════════════════════════════
✅ TAREFA FINALIZADA!
📊 Total de passos executados: 3

[Agente] Pesquisei sobre "votação do GOTY" e encontrei os
resultados na página do Google. Baseado nas manchetes...
```

## ⚠️ Segurança e Limitações

### ⚠️ AVISOS IMPORTANTES

1. **Controle Total**: O agente tem acesso completo ao seu PC
2. **Sem Confirmação**: Executa ações SEM pedir permissão
3. **Ambiente Controlado**: Use apenas em ambiente seguro
4. **Dados Sensíveis**: Pode capturar telas com informações privadas
5. **Iterações Limitadas**: Tarefas muito complexas podem não completar

### 🛡️ Recomendações de Segurança

✅ **Use para:**
- Automação de tarefas repetitivas
- Pesquisas e coleta de informações
- Testes e experimentação
- Demonstrações

❌ **NÃO use para:**
- Manipulação de dados financeiros
- Acesso a contas sensíveis
- Ambiente de produção
- Tarefas críticas de negócio

### 🔒 Proteções Implementadas

- ✅ Máximo de 20 iterações (evita loops infinitos)
- ✅ Timeout de 30s por análise
- ✅ Modo pode ser desativado a qualquer momento
- ✅ Todas as ações são logadas no chat

## 🐛 Troubleshooting

### "Agente não faz nada"

**Causa:** Ollama não está respondendo rápido o suficiente

**Solução:**
1. Verifique se Ollama está rodando: `ollama list`
2. Aumente o timeout
3. Use modelo mais leve: `llama3.2:latest`

### "Ações executam muito rápido"

**Causa:** Delay muito curto entre iterações

**Solução:**
```python
time.sleep(3)  # Aumente para 3-5 segundos
```

### "Tarefa não completa"

**Causa:** Agente não detecta conclusão

**Solução:**
1. Seja mais específico na tarefa
2. Aumente max_iterations
3. Verifique logs para ver onde parou

### "Erros de PyAutoGUI"

**Causa:** Permissões ou falha de segurança

**Solução:**
```bash
pip install --upgrade pyautogui
```

## 🔮 Futuras Melhorias

Planejadas para próximas versões:

- [ ] Suporte a modelos de visão real (GPT-4V, Llama 3.2 Vision)
- [ ] OCR para ler texto da tela
- [ ] Detecção de objetos e elementos UI
- [ ] Gravação de macros (replay de ações)
- [ ] Múltiplas tarefas paralelas
- [ ] Aprendizado com feedback
- [ ] Integração com APIs externas
- [ ] Suporte a condições e loops complexos

## 📚 Arquitetura Técnica

### Stack
- **Python 3.8+**
- **PyAutoGUI** - Controle de mouse/teclado
- **Ollama** - Análise e decisões
- **Tkinter** - Interface gráfica
- **Threading** - Execução paralela

### Fluxo de Dados

```
Usuário → Task
    ↓
ChatInterface.run_autonomous_task()
    ↓
AutonomousAgent.run_autonomous_task()
    ↓
Loop: [Captura → Analisa → Executa]
    ↓
Progress Callbacks → UI Updates
    ↓
Conclusão → Resumo com Ollama
    ↓
Resultado → Usuário
```

## 💡 Dicas de Uso

### Para Melhores Resultados

1. **Seja Específico**: "Pesquise X e me diga Y"
2. **Tarefas Curtas**: Divida tarefas grandes em etapas
3. **Monitore**: Observe o progresso em tempo real
4. **Desative quando não usar**: Economiza recursos

### Exemplos Avançados

**Multi-etapa:**
```
1. Ative modo autônomo
2. "Pesquise pela votação do GOTY"
3. Aguarde completar
4. "Agora busque análises do jogo vencedor"
5. Desative modo autônomo
```

**Com contexto:**
```
"Baseado nos resultados da busca anterior, 
 encontre vídeos no YouTube sobre o jogo"
```

## 📄 Licença

Parte do projeto Obelisk - Veja LICENSE

## 🙏 Créditos

- **PyAutoGUI**: Controle de GUI
- **Ollama**: LLM local
- **Selenium**: Automação web
- **BeautifulSoup**: Parse HTML

---

**Desenvolvido para automação inteligente e autônoma** 🤖

*"Do comando à execução completa - IA que age por você"*
