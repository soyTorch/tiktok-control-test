# syntax=docker/dockerfile:1
FROM python:3.11-slim

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    android-tools-adb \
    android-tools-fastboot \
    udev \
    libusb-1.0-0 \
    usbutils \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos de requisitos e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar scripts y entrypoint
COPY test_device.py .
COPY test_device_tcp.py .
COPY entrypoint.sh .

# Exponer el puerto del servidor ADB
EXPOSE 5037

# Variables de entorno
ENV PYTHONUNBUFFERED=1
ENV ADB_VENDOR_KEYS=/root/.android/adbkey

# Crear volúmenes para acceso USB y claves ADB
VOLUME ["/dev/bus/usb", "/root/.android"]

# Iniciar ADB al arrancar el contenedor
ENTRYPOINT ["bash", "-c", "adb start-server && ./entrypoint.sh"]
