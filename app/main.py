#!/usr/bin/env python3
"""
ADB Controller - Control remoto de dispositivos Android vía ADB
"""
import os
import subprocess
import logging
import json
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

# Configurar logging
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

def run_adb_command(command, device_id=None):
    """Ejecuta un comando ADB"""
    try:
        if device_id:
            cmd = ['adb', '-s', device_id] + command.split()
        else:
            cmd = ['adb'] + command.split()
        
        logger.info(f"Ejecutando: {' '.join(cmd)}")
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        return {
            'success': result.returncode == 0,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        }
    except subprocess.TimeoutExpired:
        logger.error(f"Timeout ejecutando comando: {command}")
        return {
            'success': False,
            'error': 'Timeout ejecutando comando'
        }
    except Exception as e:
        logger.error(f"Error ejecutando comando: {e}")
        return {
            'success': False,
            'error': str(e)
        }

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/devices', methods=['GET'])
def list_devices():
    """Lista todos los dispositivos conectados"""
    result = run_adb_command('devices -l')
    
    if not result['success']:
        return jsonify({
            'success': False,
            'error': result.get('error', result.get('stderr', 'Unknown error'))
        }), 500
    
    devices = []
    lines = result['stdout'].strip().split('\n')[1:]  # Saltar header
    
    for line in lines:
        if line.strip() and '\t' in line:
            parts = line.split('\t')
            device_id = parts[0]
            status = parts[1] if len(parts) > 1 else 'unknown'
            
            # Obtener información adicional
            info_result = run_adb_command(f'shell getprop ro.product.model', device_id)
            model = info_result['stdout'].strip() if info_result['success'] else 'Unknown'
            
            devices.append({
                'id': device_id,
                'status': status,
                'model': model
            })
    
    return jsonify({
        'success': True,
        'devices': devices,
        'count': len(devices)
    })

@app.route('/device/<device_id>/info', methods=['GET'])
def device_info(device_id):
    """Obtiene información detallada de un dispositivo"""
    info = {}
    
    props = [
        'ro.product.model',
        'ro.product.manufacturer',
        'ro.build.version.release',
        'ro.build.version.sdk',
        'ro.serialno'
    ]
    
    for prop in props:
        result = run_adb_command(f'shell getprop {prop}', device_id)
        if result['success']:
            key = prop.split('.')[-1]
            info[key] = result['stdout'].strip()
    
    return jsonify({
        'success': True,
        'device_id': device_id,
        'info': info
    })

@app.route('/device/<device_id>/command', methods=['POST'])
def execute_command(device_id):
    """Ejecuta un comando ADB en un dispositivo específico"""
    data = request.get_json()
    
    if not data or 'command' not in data:
        return jsonify({
            'success': False,
            'error': 'Comando no proporcionado'
        }), 400
    
    command = data['command']
    result = run_adb_command(command, device_id)
    
    return jsonify(result)

@app.route('/command', methods=['POST'])
def execute_global_command():
    """Ejecuta un comando ADB global (sin dispositivo específico)"""
    data = request.get_json()
    
    if not data or 'command' not in data:
        return jsonify({
            'success': False,
            'error': 'Comando no proporcionado'
        }), 400
    
    command = data['command']
    result = run_adb_command(command)
    
    return jsonify(result)

@app.route('/device/<device_id>/shell', methods=['POST'])
def shell_command(device_id):
    """Ejecuta un comando shell en el dispositivo"""
    data = request.get_json()
    
    if not data or 'command' not in data:
        return jsonify({
            'success': False,
            'error': 'Comando shell no proporcionado'
        }), 400
    
    shell_cmd = data['command']
    result = run_adb_command(f'shell {shell_cmd}', device_id)
    
    return jsonify(result)

@app.route('/device/<device_id>/install', methods=['POST'])
def install_apk(device_id):
    """Instala un APK en el dispositivo"""
    data = request.get_json()
    
    if not data or 'apk_path' not in data:
        return jsonify({
            'success': False,
            'error': 'Ruta del APK no proporcionada'
        }), 400
    
    apk_path = data['apk_path']
    result = run_adb_command(f'install -r {apk_path}', device_id)
    
    return jsonify(result)

@app.route('/device/<device_id>/screenshot', methods=['GET'])
def take_screenshot(device_id):
    """Toma una captura de pantalla del dispositivo"""
    import subprocess
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    screenshot_path = f'/app/logs/screenshot_{device_id}_{timestamp}.png'
    
    try:
        # Ejecutar screencap directamente para obtener datos binarios
        cmd = ['adb', '-s', device_id, 'shell', 'screencap', '-p']
        result = subprocess.run(
            cmd,
            capture_output=True,
            timeout=10
        )
        
        if result.returncode == 0:
            # Guardar screenshot (ADB devuelve datos binarios directamente)
            with open(screenshot_path, 'wb') as f:
                f.write(result.stdout)
            
            return jsonify({
                'success': True,
                'screenshot_path': screenshot_path,
                'message': 'Screenshot guardado exitosamente'
            })
        else:
            return jsonify({
                'success': False,
                'error': result.stderr.decode('utf-8', errors='ignore')
            }), 500
            
    except subprocess.TimeoutExpired:
        return jsonify({
            'success': False,
            'error': 'Timeout al tomar screenshot'
        }), 500
    except Exception as e:
        logger.error(f"Error tomando screenshot: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Crear directorio de logs si no existe
    os.makedirs('/app/logs', exist_ok=True)
    
    logger.info("🚀 Iniciando ADB Controller API...")
    logger.info(f"📱 Servidor ADB: {run_adb_command('version')['stdout']}")
    
    app.run(host='0.0.0.0', port=8080, debug=False)

