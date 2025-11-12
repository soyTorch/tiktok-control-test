# TikTok Control Test - UIAutomator2 + ADB Docker

Proyecto de prueba para verificar la conexión con dispositivos Android usando **UIAutomator2** y **ADB** desde un contenedor Docker.

## 📋 Requisitos

- Docker instalado
- Dispositivo Android con:
  - Depuración USB habilitada
  - Conectado por USB al ordenador (inicialmente)
  - Modo de desarrollador activado
- **En macOS**: Android Platform Tools (`brew install android-platform-tools`)

## 🚀 Construcción de la Imagen

```bash
docker build -t uiautomator2-test .
```

## 🔧 Uso

### En macOS (Recomendado - ADB sobre TCP/IP)

Docker Desktop en macOS no tiene acceso directo a USB. Usa ADB sobre TCP/IP:

**Opción 1: Script automático** (Recomendado)
```bash
# 1. Asegúrate de que tu dispositivo está conectado por USB
# 2. Ejecuta el script de configuración:
./setup_adb_tcp.sh

# 3. Ejecuta el contenedor con la IP que te muestre el script:
docker run --rm -it \
  --network host \
  -e DEVICE_ADDRESS=<IP_DISPOSITIVO>:5555 \
  uiautomator2-test
```

**Opción 2: Manual**
```bash
# 1. Conecta tu dispositivo por USB
adb devices  # Verifica que aparece

# 2. Habilita TCP/IP en puerto 5555
adb tcpip 5555

# 3. Obtén la IP del dispositivo (Ajustes > Acerca del teléfono > Estado)
# Por ejemplo: 192.168.1.100

# 4. Conecta por WiFi
adb connect 192.168.1.100:5555

# 5. Verifica la conexión
adb devices

# 6. Ahora puedes desconectar el cable USB
# 7. Ejecuta el contenedor:
docker run --rm -it \
  --network host \
  -e DEVICE_ADDRESS=192.168.1.100:5555 \
  uiautomator2-test
```

### En Linux

```bash
docker run --rm -it \
  --privileged \
  -v /dev/bus/usb:/dev/bus/usb \
  uiautomator2-test
```

### En Windows (WSL2)

```bash
# Primero conecta el dispositivo USB a WSL2
usbipd wsl attach --busid <BUSID>

# Luego ejecuta el contenedor
docker run --rm -it \
  --privileged \
  -v /dev/bus/usb:/dev/bus/usb \
  uiautomator2-test
```

## 📝 Notas Importantes

### Scripts Disponibles

El proyecto incluye dos scripts de prueba:

1. **`test_device.py`** - Script original para Linux (acceso USB directo)
2. **`test_device_tcp.py`** - Script optimizado para macOS (conexión TCP/IP)

El contenedor usa por defecto `test_device_tcp.py` que es compatible con macOS.

### Primera ejecución

Si es la primera vez que usas UIAutomator2 en tu dispositivo, necesitas instalarlo:

```bash
# Desde tu máquina host (con el dispositivo conectado):
pip install uiautomator2
python -m uiautomator2 init
```

O desde dentro del contenedor (si tienes acceso al dispositivo):

```bash
docker run --rm -it --privileged \
  -v /dev/bus/usb:/dev/bus/usb \
  uiautomator2-test \
  python -m uiautomator2 init
```

## 🧪 Qué hace el test

El script `test_device.py` realiza las siguientes verificaciones:

1. ✅ Verifica que ADB puede detectar dispositivos conectados
2. ✅ Lista todos los dispositivos encontrados con su información
3. ✅ Establece conexión con UIAutomator2
4. ✅ Obtiene información del dispositivo (marca, modelo, resolución)
5. ✅ Realiza una operación básica de prueba

## 🐛 Troubleshooting

### "No se encontraron dispositivos conectados"

- Verifica que el dispositivo está conectado con `adb devices` en el host
- Asegúrate de haber aceptado la autorización de depuración USB en el dispositivo
- Verifica que Docker se ejecuta con `--privileged`
- En Linux, verifica los permisos de `/dev/bus/usb`

### "Error al verificar UIAutomator2"

- Es posible que UIAutomator2 no esté instalado en el dispositivo
- Ejecuta: `python -m uiautomator2 init` desde el host o contenedor

### macOS: Problemas de acceso USB

- Docker en macOS no tiene acceso directo a USB
- Usa la conexión ADB sobre TCP/IP (ver sección arriba)

## 📦 Contenido del Proyecto

```
.
├── Dockerfile              # Configuración del contenedor
├── requirements.txt        # Dependencias Python
├── test_device.py          # Script de prueba (Linux/USB)
├── test_device_tcp.py      # Script de prueba (macOS/TCP)
├── setup_adb_tcp.sh        # Script de configuración para macOS
├── .gitignore              # Archivos ignorados por git
└── README.md              # Este archivo
```

## 🔗 Enlaces Útiles

- [UIAutomator2 Documentation](https://github.com/openatx/uiautomator2)
- [ADB Documentation](https://developer.android.com/tools/adb)
- [Docker Documentation](https://docs.docker.com/)

## 📄 Licencia

MIT

