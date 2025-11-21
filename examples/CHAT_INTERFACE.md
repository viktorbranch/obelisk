# Obelisk Chat Interface

Interface gráfica moderna para conversar com o Ollama e executar comandos no navegador.

## 🎯 Funcionalidades

- **Chat Interativo**: Converse naturalmente com o Ollama
- **Controle de Navegador**: Abre URLs e realiza buscas automaticamente
- **Comandos Especiais**: Controle direto via comandos
- **Interface Moderna**: Design escuro e amigável
- **Histórico**: Mantém contexto da conversa

## 📋 Requisitos

1. **Ollama instalado e rodando**
   ```bash
   # Instalar Ollama (se ainda não tiver)
   # Baixe de: https://ollama.ai
   
   # Baixar modelo (exemplo)
   ollama pull llama3.2
   
   # Verificar se está rodando
   ollama list
   ```

2. **Python 3.8+**

3. **Dependências Python**
   ```bash
   pip install requests
   ```

## 🚀 Como Usar

### Iniciar a Interface

```bash
python examples/ollama_chat_interface.py
```

### Variáveis de Ambiente (Opcional)

```bash
# Configurar URL do Ollama (padrão: http://127.0.0.1:11434)
set OLLAMA_URL=http://localhost:11434

# Configurar modelo (padrão: llama3.2:latest)
set OLLAMA_MODEL=llama3.2:latest

# Executar
python examples/ollama_chat_interface.py
```

## 💬 Exemplos de Uso

### Conversação Normal

```
Você: Olá! Como você está?
Assistente: Olá! Estou bem, obrigado por perguntar...
```

### Abrir Sites

```
Você: Abra o Google para mim
Assistente: Vou abrir o Google no navegador...
[Sistema abre https://google.com]

Você: Quero acessar o GitHub
Assistente: Abrindo GitHub...
[Sistema abre https://github.com]
```

### Realizar Buscas

```
Você: Busque sobre Python no Google
Assistente: Vou buscar sobre Python...
[Sistema abre busca do Google]

Você: Procure receitas de bolo de chocolate
[Sistema realiza busca automaticamente]
```

### Comandos Especiais

```
/browser https://google.com    # Abre URL diretamente
/search python tutorial        # Busca no Google
/clear                        # Limpa o chat
/reset                        # Reinicia a conversa
```

## ⌨️ Atalhos

- **Enter**: Envia mensagem
- **Shift + Enter**: Nova linha
- **Botão Enviar**: Envia mensagem
- **Botão Limpar**: Limpa o chat

## 🎨 Interface

A interface possui:
- **Tema escuro** para reduzir fadiga visual
- **Código de cores**:
  - 🔵 Azul: Suas mensagens
  - 🟢 Verde: Respostas do assistente
  - 🟡 Amarelo: Mensagens do sistema
  - ⚫ Cinza: Timestamps
- **Status de conexão** no canto superior direito
- **Área de chat** com scroll automático
- **Campo de entrada** expansível

## 🔧 Personalização

### Alterar Cores

Edite o método `setup_styles()` em `ollama_chat_interface.py`:

```python
self.bg_color = "#1e1e1e"      # Fundo principal
self.fg_color = "#ffffff"       # Texto
self.input_bg = "#2d2d2d"       # Fundo input
self.button_bg = "#0e639c"      # Botões
```

### Adicionar Comandos

Adicione no método `process_command()`:

```python
elif message.startswith('/seu_comando '):
    # Seu código aqui
    return "Comando executado!"
```

## 🐛 Troubleshooting

### "Não foi possível conectar ao Ollama"

1. Verifique se o Ollama está rodando:
   ```bash
   ollama list
   ```

2. Verifique a URL (padrão: http://127.0.0.1:11434)

3. Teste manualmente:
   ```bash
   curl http://127.0.0.1:11434/api/tags
   ```

### "Timeout na conexão"

- O modelo pode estar sendo baixado
- Ou a resposta está demorando muito
- Aumente o timeout em `ollama_chat_interface.py`:
  ```python
  timeout=120  # Aumentar este valor
  ```

### Navegador não abre

- Verifique se tem um navegador padrão configurado
- No Windows, configure em: Configurações > Aplicativos > Aplicativos padrão

## 📝 Notas

- O histórico da conversa é mantido na memória durante a sessão
- Use `/reset` para começar uma nova conversa
- A detecção automática de intenção de navegador funciona com palavras-chave
- URLs são extraídas automaticamente das respostas

## 🔄 Próximas Melhorias

- [ ] Salvar histórico em arquivo
- [ ] Suporte a múltiplos modelos
- [ ] Capturas de tela do navegador
- [ ] Execução de código Python
- [ ] Integração com automação de UI
- [ ] Modo voz (text-to-speech)

## 📄 Licença

Mesmo que o projeto Obelisk principal.
