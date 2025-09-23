#!/bin/bash
echo "🕹️ Iniciando Snake vs Snake..."

# Activar entorno virtual si existe
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "Entorno virtual activado"
fi

# Verificar dependencias
python3 -c "import pygame" 2>/dev/null || {
    echo "Error: pygame no encontrado. Ejecutar setup.sh primero"
    exit 1
}

# Ejecutar juego
echo "Lanzando juego..."
python3 main.py