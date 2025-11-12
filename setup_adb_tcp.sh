#!/bin/bash
# Script para configurar ADB sobre TCP/IP en macOS

echo "🔧 Configuración de ADB sobre TCP/IP para macOS"
echo "================================================"
echo ""

# Verificar que adb está instalado
if ! command -v adb &> /dev/null; then
    echo "❌ Error: adb no está instalado"
    echo "💡 Instálalo con: brew install android-platform-tools"
    exit 1
fi

echo "✅ ADB encontrado: $(which adb)"
echo ""

# Listar dispositivos
echo "1️⃣ Verificando dispositivos conectados por USB..."
adb devices -l
echo ""

# Verificar si hay dispositivos
DEVICE_COUNT=$(adb devices | grep -v "List" | grep "device$" | wc -l)

if [ "$DEVICE_COUNT" -eq 0 ]; then
    echo "❌ No se encontraron dispositivos conectados"
    echo ""
    echo "💡 Asegúrate de:"
    echo "  • Conectar tu dispositivo Android por USB"
    echo "  • Habilitar 'Depuración USB' en el dispositivo"
    echo "  • Aceptar la autorización de depuración en el dispositivo"
    exit 1
fi

echo "✅ Dispositivo(s) encontrado(s): $DEVICE_COUNT"
echo ""

# Habilitar TCP/IP
echo "2️⃣ Habilitando ADB sobre TCP/IP en puerto 5555..."
adb tcpip 5555
sleep 2
echo ""

# Obtener IP del dispositivo
echo "3️⃣ Obteniendo dirección IP del dispositivo..."
DEVICE_IP=$(adb shell ip addr show wlan0 | grep "inet " | awk '{print $2}' | cut -d/ -f1)

if [ -z "$DEVICE_IP" ]; then
    echo "⚠️  No se pudo obtener la IP automáticamente"
    echo ""
    echo "📱 Obtén manualmente la IP de tu dispositivo:"
    echo "  Android: Ajustes > Acerca del teléfono > Estado > Dirección IP"
    echo ""
    echo "Luego ejecuta:"
    echo "  adb connect <IP_DISPOSITIVO>:5555"
    echo ""
    echo "💡 Después puedes desconectar el cable USB y usar:"
    echo "  docker run --rm -it --network host -e DEVICE_ADDRESS=<IP>:5555 uiautomator2-test"
else
    echo "✅ IP del dispositivo: $DEVICE_IP"
    echo ""
    
    # Conectar por TCP/IP
    echo "4️⃣ Conectando por TCP/IP..."
    sleep 1
    adb connect ${DEVICE_IP}:5555
    sleep 2
    echo ""
    
    echo "5️⃣ Verificando conexión..."
    adb devices
    echo ""
    
    echo "✅ ¡Configuración completada!"
    echo ""
    echo "📝 Ahora puedes:"
    echo "  • Desconectar el cable USB (el dispositivo seguirá conectado por WiFi)"
    echo "  • Ejecutar el contenedor Docker:"
    echo ""
    echo "    docker run --rm -it --network host -e DEVICE_ADDRESS=${DEVICE_IP}:5555 uiautomator2-test"
    echo ""
    echo "💡 Para usar el script de Python con conexión TCP:"
    echo "    docker run --rm -it --network host -e DEVICE_ADDRESS=${DEVICE_IP}:5555 uiautomator2-test python test_device_tcp.py"
fi

