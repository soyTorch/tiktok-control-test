#!/usr/bin/env python3
"""
Script de prueba para verificar la conexión con dispositivos Android
usando uiautomator2 y adb sobre TCP/IP (ideal para macOS).
"""

import sys
import time
import os
import uiautomator2 as u2
from adbutils import adb


def get_device_address():
    """Obtiene la dirección del dispositivo desde variable de entorno o input"""
    device_addr = os.environ.get('DEVICE_ADDRESS')
    
    if not device_addr:
        print("⚠️  Variable DEVICE_ADDRESS no configurada")
        print("💡 Puedes especificarla con: -e DEVICE_ADDRESS=<IP>:5555")
        print("\nPara configurar tu dispositivo:")
        print("  1. Conecta tu dispositivo por USB a tu Mac")
        print("  2. Ejecuta: adb devices (debe aparecer)")
        print("  3. Ejecuta: adb tcpip 5555")
        print("  4. Desconecta el cable USB")
        print("  5. Obtén la IP del dispositivo (Ajustes > Acerca del teléfono > Estado > Dirección IP)")
        print("  6. Ejecuta: adb connect <IP>:5555")
        print("  7. Verifica con: adb devices")
        return None
    
    return device_addr


def check_adb_connection(device_addr=None):
    """Verifica la conexión con adb"""
    print("=" * 50)
    print("🔍 Verificando conexión ADB...")
    print("=" * 50)
    
    try:
        # Si se proporciona una dirección específica, intentar conectar
        if device_addr:
            print(f"📱 Intentando conectar a: {device_addr}")
            try:
                adb.connect(device_addr)
                time.sleep(1)
            except Exception as e:
                print(f"⚠️  Advertencia al conectar: {e}")
        
        # Listar dispositivos conectados
        devices = adb.device_list()
        
        if not devices:
            print("❌ No se encontraron dispositivos conectados")
            print("\n💡 En macOS, Docker no tiene acceso USB directo.")
            print("   Debes usar ADB sobre TCP/IP:")
            print("\n   Desde tu Mac (fuera del contenedor):")
            print("   1. adb devices  # verifica que el dispositivo está conectado")
            print("   2. adb tcpip 5555")
            print("   3. Obtén la IP del dispositivo")
            print("   4. adb connect <IP_DISPOSITIVO>:5555")
            print("   5. Ejecuta el contenedor con:")
            print("      docker run --rm -it --network host -e DEVICE_ADDRESS=<IP>:5555 uiautomator2-test")
            return None
        
        print(f"✅ Se encontraron {len(devices)} dispositivo(s):")
        for i, device in enumerate(devices, 1):
            print(f"  {i}. Serial: {device.serial}")
            print(f"     Estado: {device.state}")
        
        return devices[0].serial
    
    except Exception as e:
        print(f"❌ Error al verificar conexión ADB: {e}")
        return None


def check_uiautomator2(serial):
    """Verifica la conexión con uiautomator2"""
    print("\n" + "=" * 50)
    print("🔍 Verificando conexión UIAutomator2...")
    print("=" * 50)
    
    try:
        # Conectar al dispositivo
        print(f"📱 Conectando a: {serial}")
        d = u2.connect(serial)
        
        # Obtener información del dispositivo
        info = d.info
        
        print("✅ Conexión UIAutomator2 exitosa!")
        print(f"\n📱 Información del dispositivo:")
        print(f"  Marca: {info.get('brand', 'N/A')}")
        print(f"  Modelo: {info.get('model', 'N/A')}")
        print(f"  Versión Android: {info.get('version', 'N/A')}")
        print(f"  Resolución: {info.get('displayWidth', 'N/A')}x{info.get('displayHeight', 'N/A')}")
        
        # Probar una operación simple
        print("\n🧪 Probando operación básica (obtener tamaño de pantalla)...")
        window_size = d.window_size()
        print(f"  Tamaño de ventana: {window_size}")
        
        # Verificar si la pantalla está encendida
        screen_on = d.screen_on
        print(f"  Pantalla encendida: {'Sí' if screen_on else 'No'}")
        
        return True
    
    except Exception as e:
        print(f"❌ Error al verificar UIAutomator2: {e}")
        print("\n💡 Puede que necesites instalar uiautomator2 en el dispositivo:")
        print(f"  python -m uiautomator2 init")
        print(f"\n  O desde tu Mac:")
        print(f"  pip install uiautomator2 && python -m uiautomator2 init")
        return False


def main():
    """Función principal"""
    print("\n" + "🚀 " * 20)
    print("  TEST DE CONEXIÓN: Docker + ADB + UIAutomator2 (TCP/IP)")
    print("🚀 " * 20 + "\n")
    
    # Obtener dirección del dispositivo
    device_addr = get_device_address()
    
    # Esperar un momento para que adb server se inicie
    print("⏳ Esperando inicio del servidor ADB...")
    time.sleep(2)
    
    # Verificar conexión ADB
    serial = check_adb_connection(device_addr)
    
    if not serial:
        print("\n" + "=" * 50)
        print("❌ Test FALLIDO: No se pudo conectar via ADB")
        print("=" * 50)
        sys.exit(1)
    
    # Verificar conexión UIAutomator2
    success = check_uiautomator2(serial)
    
    if success:
        print("\n" + "=" * 50)
        print("✅ Test EXITOSO: Todas las conexiones funcionan correctamente")
        print("=" * 50)
        sys.exit(0)
    else:
        print("\n" + "=" * 50)
        print("⚠️  Test PARCIAL: ADB funciona pero UIAutomator2 necesita configuración")
        print("=" * 50)
        sys.exit(2)


if __name__ == "__main__":
    main()

