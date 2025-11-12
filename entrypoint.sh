#!/bin/bash
set -e

echo "🚀 Iniciando contenedor ADB..."
echo ""

# Esperar un momento para que el sistema reconozca los dispositivos USB
sleep 2

# Matar cualquier servidor adb existente
adb kill-server 2>/dev/null || true

# Iniciar el servidor adb
echo "📱 Iniciando servidor ADB..."
adb start-server

# Ejecutar el script de prueba
echo ""
python3 /app/test_device.py
