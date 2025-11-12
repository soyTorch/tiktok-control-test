FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Instalar ADB y dependencias
RUN apt-get update && \
    apt-get install -y \
    android-tools-adb \
    android-tools-fastboot \
    python3 \
    python3-pip \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements e instalar dependencias Python
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY app/ ./app/

# Configurar permisos USB
RUN if ! getent group plugdev >/dev/null; then groupadd -r plugdev; fi && \
    mkdir -p /etc/udev/rules.d && \
    echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="*", MODE="0664", GROUP="plugdev"' > /etc/udev/rules.d/51-android.rules

# Script de inicio
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8080

ENTRYPOINT ["/entrypoint.sh"]

