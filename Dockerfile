FROM python:3.11-slim

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    adb \
    udev \
    libusb-1.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos de requisitos e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el script de prueba
COPY test_device.py .

# Exponer puerto para adb (opcional, para conexiones TCP)
EXPOSE 5037

# Configurar variables de entorno
ENV PYTHONUNBUFFERED=1

# Comando por defecto
CMD ["python", "test_device.py"]

