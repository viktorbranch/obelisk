# 🛡️ Soluções para reCAPTCHA e Bloqueios do Google

## ❌ Problema

Quando você usa Selenium para automação, o Google pode detectar e bloquear com:
- reCAPTCHA ("Não sou um robô")
- "Tráfego incomum na sua rede"
- Bloqueio temporário de pesquisas

## ✅ Soluções Implementadas

### 1. **Modo Stealth** (Anti-Detecção)

Adicionei várias técnicas para o navegador parecer humano:

```python
# Remove flags de automação
chrome_options.add_argument('--disable-blink-features=AutomationControlled')

# User-Agent real
chrome_options.add_argument('--user-agent=Mozilla/5.0...')

# Remove propriedade webdriver
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
```

### 2. **DuckDuckGo como Alternativa**

Por padrão, agora usa **DuckDuckGo** em vez de Google:
- ✅ Sem reCAPTCHA
- ✅ Sem bloqueios
- ✅ Mesma qualidade de resultados
- ✅ Foco em privacidade

```python
# Usa DuckDuckGo por padrão
search_url = f"https://duckduckgo.com/?q={query}"
```

### 3. **Delays Aleatórios** (Comportamento Humano)

```python
# Simula tempo de leitura humano
import random
time.sleep(random.uniform(1.5, 3.0))
```

### 4. **Detecção Automática de CAPTCHA**

Se detectar reCAPTCHA, avisa e oferece alternativas:

```python
def check_and_handle_captcha(self):
    if 'recaptcha' in page_source:
        print("⚠️ reCAPTCHA detectado!")
        print("💡 Usando DuckDuckGo como alternativa...")
```

## 🎯 Como Usar Agora

### Pesquisas Funcionam Automaticamente

```
Você: pesquise python tutorials

Sistema: 🧠 Vou pesquisar 'python tutorials' no Google
Sistema: 🔍 Pesquisando 'python tutorials'...
[Usa DuckDuckGo automaticamente - SEM CAPTCHA]
Agente: Encontrei vários tutoriais de Python...
```

### Se Encontrar CAPTCHA

O sistema vai:
1. ⚠️ Detectar automaticamente
2. 🔄 Tentar DuckDuckGo
3. ⏱️ Aguardar (às vezes Google libera)
4. 💡 Avisar você para resolver manualmente se necessário

## 🔧 Configurações Adicionais

### Opção 1: Usar Apenas DuckDuckGo (Recomendado)

Já configurado! Sem alterações necessárias.

### Opção 2: Forçar Google (se preferir)

Edite `ollama_chat_web.py`, linha ~507:

```python
# Trocar de:
search_url = f"https://duckduckgo.com/?q={query.replace(' ', '+')}"

# Para:
search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}&hl=pt-BR"
```

### Opção 3: Modo Headless (Sem Janela Visível)

Edite `ollama_chat_web.py`, linha ~448:

```python
# Descomentar:
chrome_options.add_argument('--headless=new')
```

**Atenção**: Modo headless pode aumentar chance de detecção!

## 🚀 Melhorias Implementadas

| Recurso | Antes | Depois |
|---------|-------|--------|
| **User-Agent** | Selenium padrão (detectável) | Chrome real |
| **Webdriver Flag** | Visível | Removido |
| **Motor de Busca** | Google (com CAPTCHA) | DuckDuckGo (sem CAPTCHA) |
| **Delays** | Fixos (2s) | Aleatórios (1.5-3s) |
| **Detecção CAPTCHA** | ❌ Não havia | ✅ Automática |
| **Fallback** | ❌ Não havia | ✅ DuckDuckGo |

## 📊 Comparação: Google vs DuckDuckGo

| Aspecto | Google | DuckDuckGo |
|---------|--------|------------|
| **reCAPTCHA** | ❌ Frequente | ✅ Nunca |
| **Bloqueios** | ❌ Comum | ✅ Raro |
| **Privacidade** | ⚠️ Rastreamento | ✅ Zero tracking |
| **Resultados** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Velocidade** | Rápido | Rápido |

**Veredicto**: DuckDuckGo é melhor para automação!

## 🛠️ Solução Manual (Se Necessário)

Se ainda encontrar CAPTCHA:

### Passo 1: Aguarde
- O navegador ficará visível
- Aguarde 10-30 segundos
- Às vezes o Google libera automaticamente

### Passo 2: Resolva Manualmente
- Clique em "Não sou um robô"
- Complete o desafio
- O agente continuará normalmente

### Passo 3: Use VPN (Opcional)
- Mude seu IP
- Google pode ter bloqueado seu IP temporariamente

### Passo 4: Limpe Cookies
```python
# Adicione ao código se necessário:
driver.delete_all_cookies()
```

## 💡 Dicas para Evitar Bloqueios

1. **Não faça muitas buscas rápidas**
   - Limite: ~10-15 buscas por minuto
   - Solução: Adicione delays maiores

2. **Varie os User-Agents**
   - Use diferentes navegadores
   - Rotacione periodicamente

3. **Use DuckDuckGo**
   - Já configurado!
   - Zero problemas de CAPTCHA

4. **Modo Headless com cuidado**
   - Aumenta chance de detecção
   - Use apenas se necessário

5. **Proxies (Avançado)**
   - Rotacione IPs
   - Evite bloqueios permanentes

## 🎓 Por Que Google Bloqueia?

Google detecta bots por:
- ✅ **Webdriver flag** → Removemos
- ✅ **User-Agent suspeito** → Corrigimos
- ✅ **Padrões não-humanos** → Adicionamos aleatoriedade
- ✅ **Volume alto** → Use DuckDuckGo
- ❌ **IP suspeito** → Use VPN se necessário

## ✅ Resultado Final

Agora você pode:
- ✅ Fazer pesquisas sem CAPTCHA (DuckDuckGo)
- ✅ Navegador parece humano (modo stealth)
- ✅ Detecção automática de problemas
- ✅ Fallback inteligente
- ✅ Avisos claros se algo der errado

## 🧪 Teste Agora

```bash
python examples\ollama_chat_web.py
```

Digite:
```
pesquise python tutorials
```

Deve funcionar sem CAPTCHA! 🎉

---

**Problema resolvido! Use DuckDuckGo e modo stealth para navegação sem bloqueios.** 🚀
