FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Instalar ADB, Python y utilidades
RUN apt-get update && \
    apt-get install -y \
    android-tools-adb \
    android-tools-fastboot \
    python3 \
    python3-pip \
    curl \
    git \
    udev \
    && rm -rf /var/lib/apt/lists/*

# Configurar grupo y permisos USB
RUN if ! getent group plugdev >/dev/null; then groupadd -r plugdev; fi && \
    mkdir -p /etc/udev/rules.d && \
    echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="*", MODE="0666", GROUP="plugdev"' > /etc/udev/rules.d/51-android.rules && \
    udevadm control --reload-rules || true

# Crear directorio de trabajo
WORKDIR /app

# Copiar (opcional) tus scripts o código Python
COPY . .

# Entrypoint: iniciar el servidor ADB
ENTRYPOINT ["bash", "-c", "adb start-server && tail -f /dev/null"]
