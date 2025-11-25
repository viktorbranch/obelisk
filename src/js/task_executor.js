// TaskExecutor: executor autônomo de tarefas para o Obelisk
const { ObeliskAgent } = require('./agent');
const fs = require('fs');
const path = require('path');
const MEMORY_PATH = path.join(__dirname, '../../data/task_memory.json');



class TaskExecutor {
    constructor(ollamaUrl, model) {
        this.agent = new ObeliskAgent(ollamaUrl, model);
        this.loadMemory();
    }

    loadMemory() {
        try {
            const data = JSON.parse(fs.readFileSync(MEMORY_PATH, 'utf-8'));
            this.currentTask = data.currentTask;
            this.lastScreenText = data.lastScreenText;
            this.lastAction = data.lastAction;
            this.finished = data.finished;
        } catch (e) {
            this.currentTask = null;
            this.lastScreenText = '';
            this.lastAction = '';
            this.finished = false;
        }
    }

    saveMemory() {
        fs.writeFileSync(MEMORY_PATH, JSON.stringify({
            currentTask: this.currentTask,
            lastScreenText: this.lastScreenText,
            lastAction: this.lastAction,
            finished: this.finished
        }, null, 2));
    }

    async getScreenText() {
        // Captura screenshot e executa OCR Python
        const { execSync } = require('child_process');
        const vision = new (require('./vision').VisionAgent)();
        const imgFile = await vision.saveScreenshot('autotask.png');
        const ocrResult = execSync(`python "${__dirname}/ocr.py" "${imgFile}"`, { encoding: 'utf-8' });
        return ocrResult;
    }

    async decideAndAct(taskDescription) {
        // 1. Lê tela
        const screenText = await this.getScreenText();
        this.lastScreenText = screenText;
        // 2. Pergunta ao LLM qual ação tomar
        const prompt = `Você é um agente autônomo com acesso à tela do usuário.\n\nPedido do usuário: "${taskDescription}"\n\nTexto visível na tela:\n${screenText}\n\nDiga a próxima ação a ser tomada, em formato JSON:\n{\n  "action": "click|type|open_url|search|none|done",\n  "target": "(descreva o alvo: texto, botão, campo, url, etc)",\n  "value": "(texto a digitar, url, etc)",\n  "x": (opcional, coordenada x),\n  "y": (opcional, coordenada y)\n}\nSe a tarefa estiver concluída, use action: "done".`;
        const response = await this.agent.sendMessage(prompt);
        let actionObj = {};
        try {
            actionObj = JSON.parse(response.match(/\{[\s\S]*\}/)[0]);
        } catch (e) {
            actionObj = { action: 'none', target: '', value: '' };
        }
        this.lastAction = actionObj;
        this.saveMemory();
        // 3. Executa ação
        let result = '';
        try {
            if (actionObj.action === 'click' && actionObj.x && actionObj.y) {
                const { execSync } = require('child_process');
                execSync(`python "${__dirname}/automator.py" click ${actionObj.x} ${actionObj.y}`);
                result = `Clique em (${actionObj.x},${actionObj.y})`;
            } else if (actionObj.action === 'type' && actionObj.value) {
                const { execSync } = require('child_process');
                execSync(`python "${__dirname}/automator.py" write "${actionObj.value}"`);
                result = `Texto digitado: ${actionObj.value}`;
            } else if (actionObj.action === 'open_url' && actionObj.value) {
                const { execSync } = require('child_process');
                execSync(`start ${actionObj.value}`);
                result = `URL aberta: ${actionObj.value}`;
            } else if (actionObj.action === 'search' && actionObj.value) {
                const url = `https://www.google.com/search?q=${encodeURIComponent(actionObj.value)}`;
                const { execSync } = require('child_process');
                execSync(`start ${url}`);
                result = `Busca Google: ${actionObj.value}`;
            } else if (actionObj.action === 'done') {
                this.finished = true;
                result = 'Tarefa concluída!';
            } else {
                result = 'Ação não reconhecida ou insuficiente.';
            }
        } catch (err) {
            result = `Erro ao executar ação: ${err.message}`;
        }
        this.saveMemory();
        return result;
    }

    async runTask(taskDescription) {
        this.currentTask = taskDescription;
        this.finished = false;
        let result = '';
        let maxIter = 10;
        while (!this.finished && maxIter-- > 0) {
            result = await this.decideAndAct(taskDescription);
            if (this.finished) break;
        }
        this.saveMemory();
        return this.finished ? 'Tarefa finalizada!' : 'Limite de iterações atingido.';
    }
}

module.exports = { TaskExecutor };
