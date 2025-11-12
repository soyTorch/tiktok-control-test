#!/usr/bin/env python3
"""
Script de prueba para verificar la conexión con dispositivos Android
usando uiautomator2 y adb desde un contenedor Docker.
"""

import sys
import time
import uiautomator2 as u2
from adbutils import adb


def check_adb_connection():
    """Verifica la conexión con adb"""
    print("=" * 50)
    print("🔍 Verificando conexión ADB...")
    print("=" * 50)
    
    try:
        # Listar dispositivos conectados
        devices = adb.device_list()
        
        if not devices:
            print("❌ No se encontraron dispositivos conectados")
            print("\n💡 Asegúrate de:")
            print("  1. Tener un dispositivo Android conectado por USB")
            print("  2. Haber habilitado 'Depuración USB' en el dispositivo")
            print("  3. Haber aceptado la autorización en el dispositivo")
            print("  4. Ejecutar Docker con --privileged y -v /dev/bus/usb:/dev/bus/usb")
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
        print(f"  python -m uiautomator2 init {serial}")
        return False


def main():
    """Función principal"""
    print("\n" + "🚀 " * 20)
    print("  TEST DE CONEXIÓN: Docker + ADB + UIAutomator2")
    print("🚀 " * 20 + "\n")
    
    # Esperar un momento para que adb server se inicie
    print("⏳ Esperando inicio del servidor ADB...")
    time.sleep(2)
    
    # Verificar conexión ADB
    serial = check_adb_connection()
    
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

