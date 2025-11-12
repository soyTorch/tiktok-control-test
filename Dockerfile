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

# Copiar los scripts de prueba
COPY test_device.py .
COPY test_device_tcp.py .

# Exponer puerto para adb (opcional, para conexiones TCP)
EXPOSE 5037

# Configurar variables de entorno
ENV PYTHONUNBUFFERED=1

# Comando por defecto (usa el script TCP para macOS)
CMD ["python", "test_device_tcp.py"]
