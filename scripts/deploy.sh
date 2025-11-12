#!/bin/bash
set -e

echo "🚀 Desplegando ADB Controller..."

# Crear directorios necesarios
mkdir -p logs

# Dar permisos a scripts
chmod +x scripts/*.sh
chmod +x entrypoint.sh

# Construir y levantar servicios
echo "🔨 Construyendo contenedores..."
docker compose build

echo "🚀 Iniciando servicios..."
docker compose up -d

echo "⏳ Esperando a que los servicios estén listos..."
sleep 5

echo "📊 Estado de los servicios:"
docker compose ps

echo ""
echo "✅ Despliegue completado!"
echo ""
echo "📝 Comandos útiles:"
echo "  - Ver logs: docker compose logs -f"
echo "  - Ver logs de un servicio: docker compose logs -f adb-controller"
echo "  - Detener: docker compose down"
echo "  - Reiniciar: docker compose restart"
echo ""
echo "🌐 Endpoints disponibles:"
echo "  - API: http://localhost:8080"
echo "  - Health: http://localhost:8080/health"
echo "  - Dispositivos: http://localhost:8080/devices"
echo "  - Webhook: http://localhost:9090/webhook"

