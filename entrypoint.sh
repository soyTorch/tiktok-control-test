#!/bin/bash
# Entry point para seleccionar script TCP o USB según DEVICE_ADDRESS
set -e

# Reiniciar el servidor adb para evitar bloqueos por procesos previos
if command -v adb >/dev/null 2>&1; then
  adb kill-server >/dev/null 2>&1 || true
  adb start-server >/dev/null 2>&1
fi

echo "🚀 Iniciando pruebas UIAutomator2 + ADB"
if [ -n "${DEVICE_ADDRESS}" ]; then
  echo "🔌 Modo TCP/IP con DEVICE_ADDRESS=${DEVICE_ADDRESS}"
  exec python test_device_tcp.py
else
  echo "🔌 Modo USB"
  exec python test_device.py
fi
