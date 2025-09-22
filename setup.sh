#!/bin/bash
echo "🐍 Configurando Snake vs Snake - Versión Local"

# Verificar Python 3.11+
python_version=$(python3 --version 2>&1 | grep -Po '(?<=Python )\d+\.\d+')
if [[ $(echo "$python_version >= 3.11" | bc -l) != 1 ]]; then
    echo "❌ Error: Se requiere Python 3.11 o superior. Versión actual: $python_version"
    exit 1
fi

echo "✅ Python $python_version detectado"

# Crear entorno virtual
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "🔌 Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "📚 Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

# Verificar pygame
echo "🎮 Verificando pygame..."
python3 -c "import pygame; print('✅ Pygame funciona correctamente')"

echo "🚀 Setup completado! Para ejecutar:"
echo "   source venv/bin/activate"
echo "   python main.py"