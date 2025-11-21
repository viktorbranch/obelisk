# Script para criar atalho do Obelisk Chat na área de trabalho

$TargetPath = "C:\Users\tilek\OneDrive\Documentos\DEVOPS\obelisk\start_obelisk_chat.bat"
$ShortcutPath = "$env:USERPROFILE\Desktop\Obelisk Chat.lnk"
$WorkingDir = "C:\Users\tilek\OneDrive\Documentos\DEVOPS\obelisk"

$WScriptShell = New-Object -ComObject WScript.Shell
$Shortcut = $WScriptShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $TargetPath
$Shortcut.WorkingDirectory = $WorkingDir
$Shortcut.Description = "Chat com Ollama + Web Vision - Análise de páginas web"
$Shortcut.IconLocation = "C:\Windows\System32\shell32.dll,13"
$Shortcut.Save()

Write-Host "✓ Atalho 'Obelisk Chat' criado na área de trabalho!" -ForegroundColor Green
Write-Host "  Clique duas vezes no atalho para iniciar o chat." -ForegroundColor Cyan
