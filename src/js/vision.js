// Vision Module - Captura e análise de tela com IA
const screenshot = require('screenshot-desktop');
const sharp = require('sharp');
const axios = require('axios');
const fs = require('fs').promises;
const path = require('path');

class VisionAgent {
    constructor(ollamaUrl = 'http://127.0.0.1:11434', visionModel = 'llama3.2-vision:latest') {
        this.ollamaUrl = ollamaUrl;
        this.visionModel = visionModel;
        this.lastScreenshot = null;
        this.screenshotDir = path.join(__dirname, 'screenshots');
        this.ensureScreenshotDir();
    }

    async ensureScreenshotDir() {
        try {
            await fs.mkdir(this.screenshotDir, { recursive: true });
        } catch (error) {
            console.error('Erro ao criar diretório de screenshots:', error);
        }
    }

    // Captura screenshot da tela inteira
    async captureScreen() {
        try {
            const imgBuffer = await screenshot({ format: 'png' });
            this.lastScreenshot = imgBuffer;
            return imgBuffer;
        } catch (error) {
            throw new Error(`Erro ao capturar tela: ${error.message}`);
        }
    }

    // Salva screenshot em arquivo
    async saveScreenshot(filename = null) {
        try {
            const imgBuffer = await this.captureScreen();
            const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
            const fname = filename || `screenshot-${timestamp}.png`;
            const filepath = path.join(this.screenshotDir, fname);
            
            await fs.writeFile(filepath, imgBuffer);
            return filepath;
        } catch (error) {
            throw new Error(`Erro ao salvar screenshot: ${error.message}`);
        }
    }

    // Converte imagem para base64
    async imageToBase64(imgBuffer) {
        try {
            return imgBuffer.toString('base64');
        } catch (error) {
            throw new Error(`Erro ao converter imagem: ${error.message}`);
        }
    }

    // Analisa screenshot com Ollama Vision
    async analyzeScreen(question = "O que você vê nesta imagem?") {
        try {
            const imgBuffer = await this.captureScreen();
            const base64Image = await this.imageToBase64(imgBuffer);

            const response = await axios.post(`${this.ollamaUrl}/api/generate`, {
                model: this.visionModel,
                prompt: question,
                images: [base64Image],
                stream: false
            });

            return response.data.response;
        } catch (error) {
            throw new Error(`Erro ao analisar tela: ${error.message}`);
        }
    }

    // Encontra elemento na tela por descrição
    async findElement(description) {
        try {
            const question = `Localize na tela: ${description}. Descreva sua posição exata (topo, meio, fundo, esquerda, direita, centro) e o que está ao redor.`;
            return await this.analyzeScreen(question);
        } catch (error) {
            throw new Error(`Erro ao procurar elemento: ${error.message}`);
        }
    }

    // Lê texto visível na tela
    async readText() {
        try {
            const question = "Liste todo o texto visível nesta tela, organizando por seções.";
            return await this.analyzeScreen(question);
        } catch (error) {
            throw new Error(`Erro ao ler texto: ${error.message}`);
        }
    }

    // Identifica botões e elementos clicáveis
    async findClickableElements() {
        try {
            const question = "Liste todos os botões, links e elementos clicáveis visíveis, descrevendo sua posição e texto.";
            return await this.analyzeScreen(question);
        } catch (error) {
            throw new Error(`Erro ao identificar elementos: ${error.message}`);
        }
    }

    // Descreve o que está acontecendo na tela
    async describeScreen() {
        try {
            const question = "Descreva detalhadamente o que você vê na tela: qual programa está aberto, o que o usuário está fazendo, e quais ações estão disponíveis.";
            return await this.analyzeScreen(question);
        } catch (error) {
            throw new Error(`Erro ao descrever tela: ${error.message}`);
        }
    }

    // Compara duas screenshots para detectar mudanças
    async detectChanges(previousScreenshot = null) {
        try {
            const current = await this.captureScreen();
            
            if (!previousScreenshot && this.lastScreenshot) {
                previousScreenshot = this.lastScreenshot;
            }

            if (!previousScreenshot) {
                return "Primeira captura - não há screenshot anterior para comparar.";
            }

            // Usa sharp para comparar imagens
            const currentMeta = await sharp(current).metadata();
            const previousMeta = await sharp(previousScreenshot).metadata();

            if (currentMeta.width !== previousMeta.width || currentMeta.height !== previousMeta.height) {
                return "As telas têm dimensões diferentes.";
            }

            // Análise com IA
            const currentB64 = await this.imageToBase64(current);
            const previousB64 = await this.imageToBase64(previousScreenshot);

            const response = await axios.post(`${this.ollamaUrl}/api/generate`, {
                model: this.visionModel,
                prompt: "Compare estas duas imagens e descreva APENAS o que mudou entre elas.",
                images: [previousB64, currentB64],
                stream: false
            });

            this.lastScreenshot = current;
            return response.data.response;
        } catch (error) {
            throw new Error(`Erro ao detectar mudanças: ${error.message}`);
        }
    }

    // Interage com imagem - guia passo a passo
    async guideClick(targetDescription) {
        try {
            const imgBuffer = await this.captureScreen();
            const base64Image = await this.imageToBase64(imgBuffer);

            const prompt = `Vejo que o usuário quer clicar em: "${targetDescription}". 
Analise a tela e me diga:
1. Onde está localizado este elemento? (coordenadas aproximadas ou descrição de posição)
2. O elemento está visível e clicável?
3. Instruções passo a passo para clicar nele.`;

            const response = await axios.post(`${this.ollamaUrl}/api/generate`, {
                model: this.visionModel,
                prompt: prompt,
                images: [base64Image],
                stream: false
            });

            return response.data.response;
        } catch (error) {
            throw new Error(`Erro ao guiar clique: ${error.message}`);
        }
    }

    // Extrai informações específicas
    async extractInfo(query) {
        try {
            const question = `Com base nesta tela, responda: ${query}`;
            return await this.analyzeScreen(question);
        } catch (error) {
            throw new Error(`Erro ao extrair informação: ${error.message}`);
        }
    }
}

module.exports = { VisionAgent };
