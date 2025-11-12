FROM ubuntu:22.04

# Instalar ADB y dependencias USB
RUN apt-get update && apt-get install -y \
    android-tools-adb \
    android-tools-fastboot \
    udev \
    libusb-1.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Entrypoint que inicia ADB y mantiene el contenedor activo
CMD bash -c "\
  echo '🔧 Otorgando permisos a los puertos USB...' && \
  chmod -R a+rw /dev/bus/usb && \
  echo '🚀 Iniciando servidor ADB...' && \
  adb start-server && \
  echo '✅ ADB listo. Conecta tus dispositivos.' && \
  tail -f /dev/null"
