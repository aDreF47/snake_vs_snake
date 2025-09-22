@echo off
title Snake vs Snake - Setup
echo ==============================
echo Configurando entorno...
echo ==============================

REM --- Detectar Python ---
where py >nul 2>&1
if %errorlevel%==0 (
    set BASE_PYTHON=py
) else (
    where python >nul 2>&1
    if %errorlevel%==0 (
        set BASE_PYTHON=python
    ) else (
        echo [ERROR] No se encontro Python. Instala Python 3.11+
        pause
        exit /b 1
    )
)

REM --- Crear venv si no existe ---
if not exist ".venv" (
    echo Creando entorno virtual...
    %BASE_PYTHON% -m venv .venv
)

REM --- Activar entorno virtual ---
echo Activando entorno virtual...
call .venv\Scripts\activate.bat

REM --- Ya dentro del entorno, usar siempre python/pip del venv ---
echo Actualizando pip...
python -m pip install --upgrade pip setuptools wheel

echo Instalando dependencias...
pip install --only-binary=pygame -r requirements.txt

echo ==============================
echo Setup completado con exito
echo Ejecuta run.bat para iniciar el juego
echo ==============================
pause
