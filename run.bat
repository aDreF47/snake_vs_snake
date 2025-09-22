@echo off
title Snake vs Snake - Run
echo ==============================
echo Iniciando Snake vs Snake...
echo ==============================

REM --- Verificar venv ---
if not exist ".venv" (
    echo [ERROR] No se encontro entorno virtual.
    echo Ejecuta setup.bat primero.
    pause
    exit /b 1
)

REM --- Activar entorno virtual ---
call .venv\Scripts\activate.bat

REM --- Verificar dependencias ---
python -c "import pygame" >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Dependencias faltantes. Ejecuta setup.bat
    pause
    exit /b 1
)

REM --- Ejecutar juego ---
python main.py

echo ==============================
echo Juego finalizado.
echo ==============================
pause
