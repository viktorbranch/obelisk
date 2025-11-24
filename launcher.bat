@echo off
title Obelisk AI
color 0B
cls
echo.
echo  ====================================
echo         OBELISK AI LAUNCHER
echo  ====================================
echo.
echo  [*] Iniciando aplicacao...
echo  [*] Conectando ao Ollama...
echo.
cd /d "%~dp0"
start /min cmd /c "npm start"
timeout /t 2 >nul
exit
