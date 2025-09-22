FROM python:3.11-slim

# Instalar dependencias del sistema para pygame y GUI
RUN apt-get update && apt-get install -y \
    python3-dev \
    python3-pygame \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libfreetype6-dev \
    libportmidi-dev \
    libjpeg-dev \
    python3-setuptools \
    python3-numpy \
    python3-opengl \
    libgl1-mesa-dev \
    libgles2-mesa-dev \
    xvfb \
    x11-utils \
    && rm -rf /var/lib/apt/lists/*

# Configurar directorio de trabajo
WORKDIR /app

# Copiar requirements e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Configurar variables de entorno para GUI
ENV DISPLAY=:99
ENV SDL_VIDEODRIVER=x11

# Exponer puerto si necesario (para desarrollo)
EXPOSE 8000

# Comando por defecto
CMD ["python", "main.py"]