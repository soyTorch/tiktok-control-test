#!/bin/sh
set -e

REPO_DIR="/repo"
CHECK_INTERVAL=${CHECK_INTERVAL:-60}  # Segundos entre checks (default: 60)
REMOTE_URL=$(cd "$REPO_DIR" && git remote get-url origin 2>/dev/null || echo "")
BRANCH=${BRANCH:-main}

echo "🔄 Sistema de auto-actualización iniciado"
echo "📦 Repositorio: $REMOTE_URL"
echo "🌿 Rama: $BRANCH"
echo "⏱️  Intervalo de verificación: ${CHECK_INTERVAL}s"

cd "$REPO_DIR"

# Crear directorio de logs si no existe
mkdir -p "$REPO_DIR/logs"

# Función para actualizar
update_repo() {
    echo "📥 Verificando cambios..."
    
    # Hacer fetch
    git fetch origin || {
        echo "⚠️  Error al hacer fetch, saltando esta verificación..."
        return 1
    }
    
    LOCAL=$(git rev-parse @ 2>/dev/null || echo "")
    REMOTE=$(git rev-parse @{u} 2>/dev/null || echo "")
    
    if [ -z "$LOCAL" ] || [ -z "$REMOTE" ]; then
        echo "⚠️  No se puede determinar el estado del repositorio"
        return 1
    fi
    
    if [ "$LOCAL" != "$REMOTE" ]; then
        echo "🔄 Detectados cambios, actualizando..."
        echo "📥 Commit local: $LOCAL"
        echo "📥 Commit remoto: $REMOTE"
        
        # Hacer pull
        git pull origin "$BRANCH" || {
            echo "❌ Error al hacer pull"
            return 1
        }
        
        echo "🔨 Reconstruyendo contenedores..."
        docker compose -f "$REPO_DIR/docker-compose.yml" build --no-cache adb-controller || {
            echo "❌ Error al construir contenedor"
            return 1
        }
        
        echo "🔄 Reiniciando servicios..."
        docker compose -f "$REPO_DIR/docker-compose.yml" up -d --force-recreate adb-controller || {
            echo "❌ Error al reiniciar servicios"
            return 1
        }
        
        echo "✅ Actualización completada"
        echo "$(date): Actualización completada - Commit: $(git rev-parse HEAD)" >> "$REPO_DIR/logs/updates.log"
    else
        echo "✅ Ya está actualizado"
    fi
}

# Loop principal
while true; do
    sleep "$CHECK_INTERVAL"
    
    # Verificar conexión a internet
    if ! ping -c 1 github.com >/dev/null 2>&1 && ! ping -c 1 gitlab.com >/dev/null 2>&1; then
        echo "⚠️  Sin conexión a internet, saltando verificación..."
        continue
    fi
    
    update_repo
done

