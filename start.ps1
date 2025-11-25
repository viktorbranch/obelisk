$Host.UI.RawUI.WindowTitle = "Obelisk AI"
Set-Location $PSScriptRoot
Write-Host "Iniciando Obelisk AI..." -ForegroundColor Cyan
Write-Host "Conectando ao Ollama..." -ForegroundColor Yellow
Write-Host ""
npm start
