#!/bin/bash
set -e

REPO_DIR="/repo"
BRANCH=${BRANCH:-main}

echo "📥 Webhook recibido - Iniciando actualización..."

cd "$REPO_DIR"

# Crear directorio de logs si no existe
mkdir -p "$REPO_DIR/logs"

# Pull del código
echo "📥 Descargando cambios..."
git fetch origin || {
    echo "❌ Error al hacer fetch"
    exit 1
}

git checkout "$BRANCH" || {
    echo "❌ Error al cambiar de rama"
    exit 1
}

git pull origin "$BRANCH" || {
    echo "❌ Error al hacer pull"
    exit 1
}

# Reconstruir y reiniciar
echo "🔨 Reconstruyendo contenedores..."
docker compose -f "$REPO_DIR/docker-compose.yml" build --no-cache adb-controller || {
    echo "❌ Error al construir contenedor"
    exit 1
}

echo "🔄 Reiniciando servicios..."
docker compose -f "$REPO_DIR/docker-compose.yml" up -d --force-recreate adb-controller || {
    echo "❌ Error al reiniciar servicios"
    exit 1
}

echo "✅ Actualización completada"
echo "$(date): Actualización vía webhook - Commit: $(git rev-parse HEAD)" >> "$REPO_DIR/logs/updates.log"

