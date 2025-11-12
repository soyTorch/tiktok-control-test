#!/usr/bin/env python3
"""
Webhook endpoint para recibir notificaciones de actualización desde GitHub/GitLab
"""
import os
import subprocess
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', '')

@app.route('/webhook', methods=['POST'])
def webhook():
    """Endpoint para recibir webhooks de GitHub/GitLab"""
    
    # Verificar secret si está configurado
    if WEBHOOK_SECRET:
        secret = request.headers.get('X-Webhook-Secret', '')
        if secret != WEBHOOK_SECRET:
            logger.warning("Intento de webhook con secret incorrecto")
            return jsonify({'error': 'Unauthorized'}), 401
    
    # Ejecutar script de actualización
    try:
        result = subprocess.run(
            ['/repo/scripts/webhook-updater.sh'],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0:
            logger.info("Actualización completada exitosamente")
            return jsonify({
                'success': True,
                'message': 'Actualización iniciada',
                'output': result.stdout
            })
        else:
            logger.error(f"Error en actualización: {result.stderr}")
            return jsonify({
                'success': False,
                'error': result.stderr
            }), 500
            
    except Exception as e:
        logger.error(f"Error ejecutando webhook: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check para el webhook"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090, debug=False)

