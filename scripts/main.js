const { app, BrowserWindow, ipcMain, screen } = require('electron');
const path = require('path');
const { ObeliskAgent } = require('./agent');

// Configurações
const OLLAMA_URL = 'http://127.0.0.1:11434';
const MODEL = 'llama3.2:latest';

// Inicializa agente
const agent = new ObeliskAgent(OLLAMA_URL, MODEL);

// Pré-aquece o modelo ao iniciar (melhora primeira resposta)
async function warmupModel() {
    try {
        console.log('🔥 Aquecendo modelo...');
        await agent.sendMessage('Hi');
        agent.resetConversation(); // Limpa histórico do warmup
        console.log('✅ Modelo pronto!');
    } catch (error) {
        console.log('⚠️ Modelo será carregado no primeiro uso');
    }
}

let sidebarWindow = null;
let chatWindow = null;

// Cria janela da sidebar
function createSidebar() {
    const { width, height } = screen.getPrimaryDisplay().workAreaSize;
    
    sidebarWindow = new BrowserWindow({
        width: 8,
        height: 200,
        x: width - 8,
        y: Math.floor((height - 200) / 2),
        frame: false,
        transparent: true,
        alwaysOnTop: true,
        skipTaskbar: true,
        resizable: false,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        }
    });
    
    sidebarWindow.loadFile(path.join(__dirname, '..', 'sidebar.html'));
    sidebarWindow.setIgnoreMouseEvents(false);
    
    // Mantém sempre visível
    sidebarWindow.setVisibleOnAllWorkspaces(true, { visibleOnFullScreen: true });
    sidebarWindow.setAlwaysOnTop(true, 'screen-saver');
}

// Cria janela do chat
function createChat() {
    if (chatWindow) {
        chatWindow.show();
        chatWindow.focus();
        return;
    }
    
    const { width, height } = screen.getPrimaryDisplay().workAreaSize;
    
    chatWindow = new BrowserWindow({
        width: 450,
        height: height,
        x: width - 450 - 8,
        y: 0,
        frame: false,
        transparent: false,
        alwaysOnTop: true,
        skipTaskbar: false,
        resizable: false,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        }
    });
    
    chatWindow.loadFile(path.join(__dirname, '..', 'index.html'));
    
    chatWindow.on('closed', () => {
        // Não destrói a janela, apenas esconde
        chatWindow = null;
    });
    
    // Remove auto-close ao perder foco
    // chatWindow.on('blur', () => {
    //     if (chatWindow) {
    //         chatWindow.close();
    //     }
    // });
}

// Inicializa app
app.whenReady().then(() => {
    createSidebar();
    warmupModel(); // Pré-carrega o modelo em background
    
    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createSidebar();
        }
    });
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

// IPC Handlers
ipcMain.on('toggle-chat', () => {
    if (chatWindow && chatWindow.isVisible()) {
        chatWindow.hide();
    } else {
        createChat();
    }
});

ipcMain.on('close-chat', () => {
    if (chatWindow) {
        chatWindow.hide();
    }
});

ipcMain.handle('send-message', async (event, message) => {
    try {
        const response = await agent.processIntent(message);
        return {
            status: 'success',
            message: response
        };
    } catch (error) {
        return {
            status: 'error',
            message: `Erro: ${error.message}`
        };
    }
});

ipcMain.handle('send-message-stream', async (event, message) => {
    // Stream não implementado ainda - usar modo normal
    return await agent.processIntent(message);
});

console.log('🚀 Obelisk AI - Electron App');
console.log(`📡 Ollama: ${OLLAMA_URL}`);
console.log(`🤖 Modelo: ${MODEL}`);
