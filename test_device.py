#!/usr/bin/env python3
"""
Script para listar dispositivos Android conectados vía ADB
"""
import subprocess
import sys

def list_devices():
    """Lista los dispositivos Android conectados"""
    try:
        # Matar el servidor adb si está corriendo para reiniciarlo
        subprocess.run(['adb', 'kill-server'], capture_output=True)
        
        # Iniciar el servidor adb
        subprocess.run(['adb', 'start-server'], check=True, capture_output=True)
        
        # Listar dispositivos
        result = subprocess.run(
            ['adb', 'devices'],
            capture_output=True,
            text=True,
            check=True
        )
        
        print("=" * 50)
        print("DISPOSITIVOS ANDROID CONECTADOS:")
        print("=" * 50)
        print(result.stdout)
        print("=" * 50)
        
        # Contar dispositivos (excluyendo la línea de encabezado y líneas vacías)
        lines = [l for l in result.stdout.strip().split('\n') if l.strip() and 'List of devices' not in l]
        device_count = len(lines)
        
        if device_count == 0:
            print("⚠️  No se encontraron dispositivos conectados")
            sys.exit(1)
        else:
            print(f"✅ Total de dispositivos encontrados: {device_count}")
            sys.exit(0)
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando adb: {e}")
        print(f"Salida: {e.stdout}")
        print(f"Error: {e.stderr}")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ Error: adb no está instalado o no está en el PATH")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        sys.exit(1)

if __name__ == '__main__':
    list_devices()
