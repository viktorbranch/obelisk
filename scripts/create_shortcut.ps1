# Script para criar atalho do Obelisk AI na área de trabalho

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
$TargetPath = Join-Path $ProjectRoot "scripts\start_obelisk_chat.bat"
$ShortcutPath = "$env:USERPROFILE\Desktop\Obelisk AI.lnk"

$WScriptShell = New-Object -ComObject WScript.Shell
$Shortcut = $WScriptShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $TargetPath
$Shortcut.WorkingDirectory = $ProjectRoot
$Shortcut.Description = "Obelisk AI - Autonomous Agent with Vision and Web Control"
$Shortcut.IconLocation = "C:\Windows\System32\shell32.dll,13"
$Shortcut.Save()

Write-Host "✓ Atalho 'Obelisk AI' criado na área de trabalho!" -ForegroundColor Green
Write-Host "  Localização: $ShortcutPath" -ForegroundColor Cyan
Write-Host "  Clique duas vezes no atalho para iniciar." -ForegroundColor Cyan
