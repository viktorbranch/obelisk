@echo off
title Obelisk Chat - Iniciando...
cd /d "%~dp0\.."
echo.
echo ============================================
echo    OBELISK AI - AUTONOMOUS AGENT
echo ============================================
echo.
echo Iniciando aplicacao...
echo.
python src\obelisk_agent.py
if errorlevel 1 (
    echo.
    echo Tentando com python3...
    python3 src\obelisk_agent.py
)
echo.
echo Aplicacao encerrada.
pause
