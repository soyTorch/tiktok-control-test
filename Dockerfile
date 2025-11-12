FROM ubuntu:22.04

# Evitar prompts interactivos durante la instalación
ENV DEBIAN_FRONTEND=noninteractive

# Instalar adb y dependencias necesarias
RUN apt-get update && \
    apt-get install -y \
    android-tools-adb \
    android-tools-fastboot \
    udev \
    python3 \
    && rm -rf /var/lib/apt/lists/*

# Crear reglas udev básicas para dispositivos Android
RUN echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="*", MODE="0666"' > /etc/udev/rules.d/51-android.rules

# Directorio de trabajo
WORKDIR /app

# Copiar scripts
COPY test_device.py /app/
COPY entrypoint.sh /app/

# Hacer ejecutable el entrypoint
RUN chmod +x /app/entrypoint.sh

# Ejecutar el script de prueba
ENTRYPOINT ["/app/entrypoint.sh"]
