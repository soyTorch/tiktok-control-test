#!/bin/bash
set -e

echo "🔄 Actualización manual iniciada..."

cd "$(dirname "$0")/.."

# Pull del código
echo "📥 Descargando cambios..."
git fetch origin
git pull origin main

# Reconstruir y reiniciar
echo "🔨 Reconstruyendo contenedores..."
docker compose build --no-cache adb-controller

echo "🔄 Reiniciando servicios..."
docker compose up -d --force-recreate adb-controller

echo "✅ Actualización completada"
echo "$(date): Actualización manual - Commit: $(git rev-parse HEAD)" >> logs/updates.log

