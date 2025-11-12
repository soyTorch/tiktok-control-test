#!/bin/bash
set -e

echo "🔧 Configurando permisos USB..."
chmod -R a+rw /dev/bus/usb || true

echo "🧹 Limpiando servidor ADB anterior..."
adb kill-server || true

echo "🚀 Iniciando servidor ADB..."
adb start-server

echo "📱 Listando dispositivos conectados..."
adb devices -l

echo "🌐 Iniciando aplicación..."
exec python3 -m app.main

