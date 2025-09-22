#!/bin/bash
echo "🕹️ Iniciando Snake vs Snake..."

# Opción 1: Docker (recomendado)
if command -v docker &> /dev/null && [ -f "docker-compose.yml" ]; then
    echo "Docker detectado - usando containerización..."
    docker-compose up --build
    exit 0
fi

# Activar entorno virtual si existe
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "Entorno virtual activado"
fi

# Verificar dependencias
python3 -c "import pygame" 2>/dev/null || {
    echo "Error: pygame no encontrado. Ejecutar scripts/setup.sh primero"
    exit 1
}

# Ejecutar juego
echo "Lanzando juego..."
python3 main.py