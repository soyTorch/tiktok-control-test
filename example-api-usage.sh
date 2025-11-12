#!/bin/bash
# Ejemplos de uso de la API

API_URL="http://localhost:8080"

echo "🔍 Health Check..."
curl -s "$API_URL/health" | jq '.'

echo -e "\n📱 Listando dispositivos..."
curl -s "$API_URL/devices" | jq '.'

echo -e "\n📱 Información de dispositivo (reemplaza <device_id>):"
# curl -s "$API_URL/device/<device_id>/info" | jq '.'

echo -e "\n💻 Ejecutar comando shell (reemplaza <device_id>):"
# curl -s -X POST "$API_URL/device/<device_id>/shell" \
#   -H "Content-Type: application/json" \
#   -d '{"command": "echo hello"}' | jq '.'

echo -e "\n📸 Captura de pantalla (reemplaza <device_id>):"
# curl -s "$API_URL/device/<device_id>/screenshot" | jq '.'

