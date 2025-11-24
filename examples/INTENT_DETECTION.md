# 🎯 Demonstração de Detecção Inteligente de Intenções

## 🧠 Como Funciona

O Obelisk AI agora possui um **processador de intenções** que detecta automaticamente o que você quer fazer, sem necessidade de comandos específicos ou sintaxe especial!

## ✨ Linguagem 100% Natural

### Antes vs Agora

**ANTES** (comandos específicos):
```
Você: /browser https://www.google.com
Você: /analyze https://news.google.com
Você: /news
```

**AGORA** (linguagem natural):
```
Você: abre o google
Você: vai no google notícias  
Você: me dá as últimas notícias
```

O agente **entende**, **executa** e **reporta** automaticamente!

## 🎪 Demonstração ao Vivo

### 1. Abrir Sites

```
Você: abre o google

Sistema: 🧠 Entendi que você quer abrir google
Sistema: 🔄 Iniciando navegador Chrome...
Sistema: ✓ Chrome pronto!
Sistema: 🌐 Abrindo Google...
Agente: Abri o Google para você! Está vendo a página inicial com a barra de pesquisa.
```

**Funciona com**:
- "vai no youtube"
- "abre o gmail"
- "acessa o github"
- "entra no whatsapp"
- "abre netflix"

### 2. Pesquisar no Google

```
Você: pesquise python machine learning

Sistema: 🧠 Vou pesquisar 'python machine learning' no Google
Sistema: 🔍 Pesquisando 'python machine learning' no Google...
Agente: Encontrei vários resultados sobre Python e Machine Learning:

PRINCIPAIS RESULTADOS:
1. Machine Learning in Python - Scikit-learn
2. Python Machine Learning Tutorial - W3Schools
3. Introduction to Machine Learning with Python
4. TensorFlow - Python Deep Learning Framework
...

Quer que eu abra algum desses links ou explique mais sobre o tema?
```

**Também funciona**:
- "busca receitas de bolo"
- "procura notebooks baratos"
- "pesquisa horário do filme"
- "google quanto custa um iphone"

### 3. Resumo de Notícias

```
Você: preciso de um resumo das notícias

Sistema: 🧠 Vou buscar as principais notícias para você
Sistema: 📰 Coletando notícias dos principais sites...
Sistema: 🌐 Acessando https://news.google.com...
Sistema: 🌐 Acessando https://g1.globo.com...
Agente: Aqui está um resumo das principais notícias de hoje:

MANCHETES DE DESTAQUE:
1. Congresso aprova novo projeto de lei sobre IA
2. Dólar fecha em alta após decisão do Fed
3. Brasil vence amistoso por 2 a 0
4. Novo lançamento da Apple quebra recordes
5. Cientistas descobrem nova espécie na Amazônia
...

Resumo: As principais notícias cobrem economia, política, esportes e tecnologia...
```

**Variações que funcionam**:
- "me dá as últimas notícias"
- "quais são as manchetes de hoje"
- "resumo das novidades"

### 4. Controle do Navegador

```
Você: fecha o chrome

Sistema: 🧠 Vou fechar o navegador
Sistema: 🔴 Fechando navegador...
Agente: Fechei o navegador Chrome.
```

**Também funciona**:
- "fecha essa aba"
- "fecha a página"
- "encerra o navegador"

### 5. Abrir Programas

```
Você: abra a calculadora

Sistema: 🧠 Vou abrir calculadora
Sistema: 🚀 Abrindo calculadora...
Agente: Abri a calculadora para você!
```

**Programas que reconhece**:
- Calculadora
- Bloco de Notas / Notepad
- Paint
- Explorador de Arquivos
- Chrome, Firefox, Edge
- Word, Excel, PowerPoint
- CMD / Terminal / PowerShell

### 6. Screenshots

```
Você: tira um screenshot

Sistema: 🧠 Vou tirar uma captura de tela
Sistema: 📸 Capturando tela...
Sistema: ✓ Screenshot salvo: screenshot_20251124_103045.png
Agente: Tirei um screenshot e salvei como 'screenshot_20251124_103045.png'.
```

## 🎨 Sites Pré-Configurados

O agente conhece automaticamente esses sites:

### Redes Sociais
- Google, YouTube, Facebook, Twitter/X
- Instagram, LinkedIn, GitHub
- Reddit, Stack Overflow

### Comunicação
- Gmail, WhatsApp Web, Outlook

### Compras & Serviços
- Amazon, Mercado Livre
- Netflix

### Notícias
- Google News, G1, UOL
- Folha, Estadão, CNN, BBC

### IA & Ferramentas
- ChatGPT, Claude, Gemini
- Wikipedia, Bing, Yahoo

## 🔥 Tarefas Complexas

### Exemplo 1: Pesquisa + Análise

```
Você: pesquise "melhores notebooks 2024" e me diga qual é o melhor custo-benefício

Sistema: 🧠 Vou pesquisar 'melhores notebooks 2024' no Google
Sistema: 🔍 Pesquisando...
Agente: Encontrei várias análises e reviews. Vou abrir os principais artigos para analisar...

[Agente lê várias páginas]

Agente: Baseado nas análises que li, os notebooks com melhor custo-benefício em 2024 são:

1. **Lenovo IdeaPad 3i** - R$ 2.799
   - Intel i5 12ª geração
   - 8GB RAM
   - SSD 256GB
   - Melhor para uso diário

2. **Acer Aspire 5** - R$ 3.299
   - Ryzen 5
   - 16GB RAM  
   - SSD 512GB
   - Melhor para trabalho pesado

Quer que eu pesquise preços em lojas específicas?
```

### Exemplo 2: Notícias + Contexto

```
Você: me dê um resumo das notícias sobre tecnologia

Sistema: 🧠 Vou buscar notícias sobre tecnologia
[Coleta de vários sites]

Agente: Principais notícias de tecnologia hoje:

**IA e Machine Learning**
- OpenAI anuncia GPT-5 com capacidades revolucionárias
- Google Gemini agora disponível em português

**Hardware**
- Apple lança novo MacBook Pro com chip M4
- NVIDIA anuncia RTX 5090 para 2025

**Software**
- Microsoft integra Copilot em todo Windows 11
- Chrome 120 traz melhorias de performance

Quer detalhes sobre alguma dessas notícias?
```

## ⚡ Níveis de Confiança

O sistema analisa a confiança antes de executar:

| Confiança | Ação |
|-----------|------|
| **95%+** | Executa imediatamente (ex: "abre o google") |
| **70-95%** | Executa mas confirma (ex: "google" sozinho) |
| **< 70%** | Envia para Ollama processar (conversa normal) |

## 🎯 Quando Usa Detecção vs Ollama

### Usa Detecção Automática:
- ✅ Comandos de ação claros ("abra", "pesquise", "feche")
- ✅ Menções de sites conhecidos
- ✅ Palavras-chave específicas ("notícias", "screenshot")

### Usa Ollama (conversa):
- ✅ Perguntas conceituais ("o que é Python?")
- ✅ Explicações ("como funciona X?")
- ✅ Análises e opiniões ("qual o melhor?")
- ✅ Quando incerto (confiança < 60%)

### Usa Ambos:
- ✅ Executa ação + processa com Ollama
- ✅ Exemplo: Busca no Google → Ollama analisa resultados
- ✅ Exemplo: Abre site → Ollama extrai informação

## 🧪 Testando

Execute o teste do processador:

```bash
python examples/intent_processor.py
```

Saída esperada:
```
🧪 Testando detecção de intenções:

📝 'abre o google'
   → Entendi que você quer abrir google
   → Ação: OPEN_BROWSER (confiança: 90%)

📝 'pesquise python'
   → Vou pesquisar 'python' no Google
   → Ação: SEARCH (confiança: 95%)

📝 'me dá um resumo das notícias'
   → Vou buscar as principais notícias para você
   → Ação: NEWS_SUMMARY (confiança: 90%)
...
```

## 🔮 Próximos Passos

Planejado para próximas versões:

- 📧 Envio de emails
- 📁 Manipulação de arquivos
- 🎵 Controle de mídia (play, pause, volume)
- 📊 Criação de documentos
- 💬 Integração com redes sociais
- 🗓️ Agendamento de tarefas

---

**O agente está ficando cada vez mais inteligente! 🚀**

Digite em linguagem natural e deixe ele entender e executar automaticamente.
