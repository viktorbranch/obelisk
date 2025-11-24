// Obelisk Agent - Core functionality in JavaScript
const axios = require('axios');
const { exec } = require('child_process');
const { promisify } = require('util');
const execAsync = promisify(exec);
const { VisionAgent } = require('./vision');

class ObeliskAgent {
    constructor(ollamaUrl = 'http://127.0.0.1:11434', model = 'llama3.2:latest') {
        this.ollamaUrl = ollamaUrl;
        this.model = model;
        this.conversationHistory = [];
        this.intentProcessor = new IntentProcessor();
        this.vision = new VisionAgent(ollamaUrl, 'llama3.2-vision:latest');
    }

    // Chat com Ollama (otimizado para respostas rápidas)
    async sendMessage(message) {
        // Adiciona contexto para respostas curtas
        const optimizedMessage = `${message}\n\n(Responda de forma BREVE e DIRETA em até 2 linhas)`;
        
        this.conversationHistory.push({
            role: 'user',
            content: optimizedMessage
        });

        try {
            const response = await axios.post(`${this.ollamaUrl}/api/generate`, {
                model: this.model,
                prompt: optimizedMessage,
                stream: false,
                options: {
                    num_predict: 100,
                    temperature: 0.7,
                    top_p: 0.9,
                    num_ctx: 2048
                }
            }, {
                timeout: 30000
            });

            const assistantMessage = response.data.response;
            
            this.conversationHistory.push({
                role: 'assistant',
                content: assistantMessage
            });

            return assistantMessage.trim();
        } catch (error) {
            if (error.code === 'ECONNABORTED') {
                throw new Error('⏱️ Timeout (30s). O modelo pode estar carregando pela primeira vez. Tente novamente.');
            }
            if (error.code === 'ECONNREFUSED') {
                throw new Error('🔌 Ollama não está rodando. Inicie com: ollama serve');
            }
            throw new Error(`❌ Erro Ollama: ${error.message}`);
        }
    }

    // Reset conversa
    resetConversation() {
        this.conversationHistory = [];
    }

    // Processa intenção e executa ação
    async processIntent(message) {
        const intent = this.intentProcessor.detectIntent(message);
        
        // Respostas rápidas para ações diretas (sem precisar chamar Ollama)
        if (intent.confidence > 0.8) {
            return await this.executeAction(intent);
        }
        
        // Fallback para chat normal
        return await this.sendMessage(message);
    }

    // Executa ação baseada na intenção
    async executeAction(intent) {
        const { action, params } = intent;

        try {
            switch (action) {
                case 'OPEN_BROWSER':
                    return await this.openUrl(params.url, params.name);
                
                case 'SEARCH':
                    return await this.searchGoogle(params.query);
                
                case 'OPEN_APP':
                    return await this.openProgram(params.app, params.name);
                
                case 'CLOSE_APP':
                    return await this.closeProgram(params.name);
                
                case 'SCREENSHOT':
                    return await this.takeScreenshot();
                
                case 'ANALYZE_SCREEN':
                    return await this.analyzeScreen(params.question);
                
                case 'FIND_ELEMENT':
                    return await this.findElement(params.description);
                
                case 'READ_SCREEN':
                    return await this.readScreen();
                
                case 'DESCRIBE_SCREEN':
                    return await this.describeScreen();
                
                case 'CLICK_ELEMENT':
                    return await this.clickElement(params.description);
                
                default:
                    return await this.sendMessage(params.userMessage || '');
            }
        } catch (error) {
            return `❌ Erro: ${error.message}`;
        }
    }

    // Abre URL no navegador padrão
    async openUrl(url, name) {
        try {
            const command = process.platform === 'win32' 
                ? `start ${url}` 
                : process.platform === 'darwin'
                ? `open ${url}`
                : `xdg-open ${url}`;
            
            await execAsync(command);
            return `✓ ${name} aberto`;
        } catch (error) {
            throw new Error(`Não foi possível abrir ${name}`);
        }
    }

    // Busca no Google
    async searchGoogle(query) {
        const searchUrl = `https://www.google.com/search?q=${encodeURIComponent(query)}`;
        return await this.openUrl(searchUrl, `Busca: ${query}`);
    }

    // Abre programa
    async openProgram(program, name) {
        try {
            const command = process.platform === 'win32'
                ? `start ${program}`
                : program;
            
            await execAsync(command);
            return `✓ ${name} aberto`;
        } catch (error) {
            throw new Error(`Não foi possível abrir ${name}`);
        }
    }

    // Fecha programa
    async closeProgram(name) {
        try {
            const command = process.platform === 'win32'
                ? `taskkill /IM ${name}.exe /F`
                : `pkill ${name}`;
            
            await execAsync(command);
            return `✓ ${name} fechado`;
        } catch (error) {
            throw new Error(`Não foi possível fechar ${name}`);
        }
    }

    // Screenshot (requer biblioteca adicional)
    async takeScreenshot() {
        try {
            const filepath = await this.vision.saveScreenshot();
            return `✓ Screenshot salvo em: ${filepath}`;
        } catch (error) {
            throw new Error(`Erro ao capturar tela: ${error.message}`);
        }
    }

    // Analisa o que está na tela
    async analyzeScreen(question = "O que você vê na tela?") {
        try {
            const analysis = await this.vision.analyzeScreen(question);
            return `🔍 Análise da tela:\n${analysis}`;
        } catch (error) {
            throw new Error(`Erro ao analisar tela: ${error.message}`);
        }
    }

    // Encontra elemento específico
    async findElement(description) {
        try {
            const location = await this.vision.findElement(description);
            return `📍 ${description}:\n${location}`;
        } catch (error) {
            throw new Error(`Erro ao procurar elemento: ${error.message}`);
        }
    }

    // Lê texto da tela
    async readScreen() {
        try {
            const text = await this.vision.readText();
            return `📖 Texto na tela:\n${text}`;
        } catch (error) {
            throw new Error(`Erro ao ler tela: ${error.message}`);
        }
    }

    // Descreve tela completa
    async describeScreen() {
        try {
            const description = await this.vision.describeScreen();
            return `🖥️ Descrição:\n${description}`;
        } catch (error) {
            throw new Error(`Erro ao descrever tela: ${error.message}`);
        }
    }

    // Guia como clicar em elemento
    async clickElement(description) {
        try {
            const guide = await this.vision.guideClick(description);
            return `👆 Como clicar em "${description}":\n${guide}`;
        } catch (error) {
            throw new Error(`Erro ao guiar clique: ${error.message}`);
        }
    }
}

class IntentProcessor {
    constructor() {
        this.knownSites = {
            'google': { url: 'https://www.google.com', name: 'Google' },
            'youtube': { url: 'https://www.youtube.com', name: 'YouTube' },
            'facebook': { url: 'https://www.facebook.com', name: 'Facebook' },
            'twitter': { url: 'https://www.twitter.com', name: 'Twitter' },
            'x': { url: 'https://www.x.com', name: 'X' },
            'instagram': { url: 'https://www.instagram.com', name: 'Instagram' },
            'linkedin': { url: 'https://www.linkedin.com', name: 'LinkedIn' },
            'github': { url: 'https://www.github.com', name: 'GitHub' },
            'gmail': { url: 'https://mail.google.com', name: 'Gmail' },
            'whatsapp': { url: 'https://web.whatsapp.com', name: 'WhatsApp' },
            'reddit': { url: 'https://www.reddit.com', name: 'Reddit' },
            'amazon': { url: 'https://www.amazon.com.br', name: 'Amazon' },
            'mercado livre': { url: 'https://www.mercadolivre.com.br', name: 'Mercado Livre' },
            'netflix': { url: 'https://www.netflix.com', name: 'Netflix' },
            'wikipedia': { url: 'https://www.wikipedia.org', name: 'Wikipedia' },
            'stackoverflow': { url: 'https://stackoverflow.com', name: 'Stack Overflow' },
            'g1': { url: 'https://g1.globo.com', name: 'G1' },
            'uol': { url: 'https://www.uol.com.br', name: 'UOL' },
            'chatgpt': { url: 'https://chat.openai.com', name: 'ChatGPT' },
            'claude': { url: 'https://claude.ai', name: 'Claude' },
            'gemini': { url: 'https://gemini.google.com', name: 'Gemini' }
        };

        this.programs = {
            'calculadora': { cmd: 'calc', name: 'Calculadora' },
            'calc': { cmd: 'calc', name: 'Calculadora' },
            'bloco de notas': { cmd: 'notepad', name: 'Bloco de Notas' },
            'notepad': { cmd: 'notepad', name: 'Notepad' },
            'paint': { cmd: 'mspaint', name: 'Paint' },
            'explorador': { cmd: 'explorer', name: 'Explorador' },
            'explorer': { cmd: 'explorer', name: 'Explorer' },
            'chrome': { cmd: 'chrome', name: 'Chrome' },
            'firefox': { cmd: 'firefox', name: 'Firefox' },
            'edge': { cmd: 'msedge', name: 'Edge' },
            'word': { cmd: 'winword', name: 'Word' },
            'excel': { cmd: 'excel', name: 'Excel' },
            'cmd': { cmd: 'cmd', name: 'CMD' },
            'terminal': { cmd: 'cmd', name: 'Terminal' },
            'powershell': { cmd: 'powershell', name: 'PowerShell' }
        };

        this.intentPatterns = {
            openSite: ['abra', 'abre', 'abrir', 'vai no', 'vai na', 'vai para', 'acessa', 'acessar', 'acesse', 'entra no', 'entra na'],
            search: ['pesquise', 'pesquisa', 'pesquisar', 'busque', 'busca', 'buscar', 'procure', 'procura', 'procurar', 'google', 'googla'],
            screenshot: ['screenshot', 'captura', 'print', 'printar', 'foto da tela', 'tira um print', 'tira uma foto'],
            close: ['feche', 'fechar', 'fecha', 'encerra', 'encerrar', 'sai do', 'sai da'],
            openProgram: ['abre o', 'abre a', 'abra o', 'abra a', 'inicia', 'iniciar', 'roda', 'rodar', 'executa', 'executar'],
            analyzeScreen: ['o que você vê', 'o que está na tela', 'descreva a tela', 'analise a tela', 'veja a tela'],
            findElement: ['onde está', 'encontre', 'procure na tela', 'localize', 'cadê'],
            readScreen: ['leia a tela', 'leia o texto', 'que texto tem', 'lê a tela', 'ler tela'],
            describeScreen: ['descreva', 'o que tem na tela', 'me conte o que vê'],
            clickElement: ['clique em', 'clica em', 'clicar em', 'aperte', 'pressione']
        };
    }

    detectIntent(message) {
        const msg = message.toLowerCase().trim();

        // Detecta abertura de site
        for (const pattern of this.intentPatterns.openSite) {
            if (msg.includes(pattern)) {
                for (const [key, site] of Object.entries(this.knownSites)) {
                    if (msg.includes(key)) {
                        return {
                            action: 'OPEN_BROWSER',
                            params: { url: site.url, name: site.name },
                            confidence: 0.95
                        };
                    }
                }
            }
        }

        // Detecta busca
        for (const pattern of this.intentPatterns.search) {
            if (msg.startsWith(pattern)) {
                const query = msg.replace(new RegExp(`^${pattern}\\s+`), '').trim();
                if (query) {
                    return {
                        action: 'SEARCH',
                        params: { query },
                        confidence: 0.9
                    };
                }
            }
        }

        // Detecta abertura de programa
        for (const pattern of this.intentPatterns.openProgram) {
            if (msg.includes(pattern)) {
                for (const [key, prog] of Object.entries(this.programs)) {
                    if (msg.includes(key)) {
                        return {
                            action: 'OPEN_APP',
                            params: { app: prog.cmd, name: prog.name },
                            confidence: 0.9
                        };
                    }
                }
            }
        }

        // Detecta fechar programa
        for (const pattern of this.intentPatterns.close) {
            if (msg.includes(pattern)) {
                for (const [key, prog] of Object.entries(this.programs)) {
                    if (msg.includes(key)) {
                        return {
                            action: 'CLOSE_APP',
                            params: { name: key },
                            confidence: 0.85
                        };
                    }
                }
            }
        }

        // Detecta screenshot
        for (const pattern of this.intentPatterns.screenshot) {
            if (msg.includes(pattern)) {
                return {
                    action: 'SCREENSHOT',
                    params: {},
                    confidence: 0.9
                };
            }
        }

        // Detecta análise de tela
        for (const pattern of this.intentPatterns.analyzeScreen) {
            if (msg.includes(pattern)) {
                return {
                    action: 'ANALYZE_SCREEN',
                    params: { question: message },
                    confidence: 0.85
                };
            }
        }

        // Detecta busca de elemento
        for (const pattern of this.intentPatterns.findElement) {
            if (msg.includes(pattern)) {
                const description = msg.replace(new RegExp(pattern, 'gi'), '').trim();
                if (description) {
                    return {
                        action: 'FIND_ELEMENT',
                        params: { description },
                        confidence: 0.85
                    };
                }
            }
        }

        // Detecta leitura de tela
        for (const pattern of this.intentPatterns.readScreen) {
            if (msg.includes(pattern)) {
                return {
                    action: 'READ_SCREEN',
                    params: {},
                    confidence: 0.9
                };
            }
        }

        // Detecta descrição de tela
        for (const pattern of this.intentPatterns.describeScreen) {
            if (msg.includes(pattern)) {
                return {
                    action: 'DESCRIBE_SCREEN',
                    params: {},
                    confidence: 0.88
                };
            }
        }

        // Detecta clique em elemento
        for (const pattern of this.intentPatterns.clickElement) {
            if (msg.includes(pattern)) {
                const description = msg.replace(new RegExp(pattern, 'gi'), '').trim();
                if (description) {
                    return {
                        action: 'CLICK_ELEMENT',
                        params: { description },
                        confidence: 0.85
                    };
                }
            }
        }

        // Nenhuma intenção clara detectada
        return {
            action: 'CHAT',
            params: { userMessage: message },
            confidence: 0.5
        };
    }
}

module.exports = { ObeliskAgent, IntentProcessor };
