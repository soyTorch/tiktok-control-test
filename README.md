# ADB Controller - Control Remoto de Dispositivos Android

Sistema para controlar múltiples dispositivos Android vía ADB desde un servidor Ubuntu, con auto-actualización y acceso USB privilegiado.

## 🚀 Características

- ✅ Control remoto de múltiples dispositivos Android vía ADB
- ✅ API REST para gestionar dispositivos
- ✅ Auto-actualización automática (polling o webhook)
- ✅ Acceso USB privilegiado mediante Docker
- ✅ Logging y monitoreo
- ✅ Health checks y reinicio automático

## 📋 Requisitos

- Ubuntu Server (o similar)
- Docker y Docker Compose instalados
- Dispositivos Android conectados vía USB con depuración USB habilitada
- Git configurado con acceso al repositorio

## 🔧 Instalación

1. Clonar el repositorio en el servidor:
```bash
git clone <tu-repositorio> /opt/adb-controller
cd /opt/adb-controller
```

2. Ejecutar el script de despliegue:
```bash
./scripts/deploy.sh
```

3. Verificar que los servicios estén corriendo:
```bash
docker compose ps
```

## 🔄 Sistema de Auto-actualización

El proyecto incluye dos métodos de auto-actualización:

### Método 1: Polling (Automático)

El contenedor `updater` verifica cada 60 segundos si hay cambios en el repositorio remoto. Si detecta cambios, automáticamente:
1. Hace pull del código
2. Reconstruye el contenedor
3. Reinicia el servicio

Configuración en `docker-compose.yml`:
```yaml
environment:
  - CHECK_INTERVAL=60  # Segundos entre verificaciones
  - BRANCH=main
```

### Método 2: Webhook (Recomendado)

Configura un webhook en GitHub/GitLab que apunte a:
```
http://tu-servidor:9090/webhook
```

**GitHub:**
1. Ve a Settings → Webhooks → Add webhook
2. URL: `http://tu-servidor:9090/webhook`
3. Content type: `application/json`
4. Events: `Push`
5. (Opcional) Secret: Configura `WEBHOOK_SECRET` en `.env`

**GitLab:**
1. Ve a Settings → Webhooks
2. URL: `http://tu-servidor:9090/webhook`
3. Trigger: `Push events`
4. (Opcional) Secret token: Configura `WEBHOOK_SECRET` en `.env`

## 📡 API Endpoints

### Health Check
```bash
GET http://localhost:8080/health
```

### Listar Dispositivos
```bash
GET http://localhost:8080/devices
```

### Información de un Dispositivo
```bash
GET http://localhost:8080/device/<device_id>/info
```

### Ejecutar Comando ADB
```bash
POST http://localhost:8080/device/<device_id>/command
Content-Type: application/json

{
  "command": "shell pm list packages"
}
```

### Ejecutar Comando Shell
```bash
POST http://localhost:8080/device/<device_id>/shell
Content-Type: application/json

{
  "command": "ls /sdcard"
}
```

### Instalar APK
```bash
POST http://localhost:8080/device/<device_id>/install
Content-Type: application/json

{
  "apk_path": "/path/to/app.apk"
}
```

### Captura de Pantalla
```bash
GET http://localhost:8080/device/<device_id>/screenshot
```

## 📝 Comandos Útiles

### Ver logs
```bash
# Todos los servicios
docker compose logs -f

# Solo el controlador ADB
docker compose logs -f adb-controller

# Solo el updater
docker compose logs -f updater
```

### Actualización manual
```bash
./scripts/update-manual.sh
```

### Reiniciar servicios
```bash
docker compose restart
```

### Detener servicios
```bash
docker compose down
```

### Ver dispositivos conectados (desde el host)
```bash
docker compose exec adb-controller adb devices
```

## 🔒 Seguridad

- El contenedor requiere privilegios (`privileged: true`) para acceder a USB
- Configura `WEBHOOK_SECRET` en `.env` para proteger el endpoint de webhook
- Considera usar un reverse proxy (nginx) con SSL/TLS para producción
- Restringe el acceso a los puertos 8080 y 9090 mediante firewall

## 🐛 Troubleshooting

### Los dispositivos no aparecen

1. Verifica que los dispositivos estén conectados:
```bash
docker compose exec adb-controller adb devices
```

2. Verifica permisos USB:
```bash
ls -la /dev/bus/usb
```

3. Reinicia el servidor ADB:
```bash
docker compose exec adb-controller adb kill-server
docker compose exec adb-controller adb start-server
```

### El updater no funciona

1. Verifica los logs:
```bash
docker compose logs updater
```

2. Verifica que el repositorio tenga el remote configurado:
```bash
git remote -v
```

3. Verifica conectividad:
```bash
docker compose exec updater ping -c 3 github.com
```

## 📁 Estructura del Proyecto

```
.
├── app/
│   ├── __init__.py
│   ├── main.py          # API principal
│   └── webhook.py       # Endpoint de webhook
├── scripts/
│   ├── deploy.sh        # Script de despliegue
│   ├── update-check.sh  # Script de polling
│   ├── update-manual.sh # Actualización manual
│   └── webhook-updater.sh # Actualización vía webhook
├── logs/                # Logs de la aplicación
├── docker-compose.yml   # Configuración Docker Compose
├── Dockerfile           # Imagen del controlador ADB
├── Dockerfile.webhook   # Imagen del webhook
├── entrypoint.sh        # Script de inicio
└── requirements.txt     # Dependencias Python
```

## 📄 Licencia

MIT

