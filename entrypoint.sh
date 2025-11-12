#!/bin/bash
set -e

echo "Iniciando servidor ADB..."
adb start-server

# Mantiene el contenedor activo
tail -f /dev/null
