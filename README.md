# TikTok Control Test - UIAutomator2 + ADB Docker

Proyecto de prueba para verificar la conexión con dispositivos Android usando **UIAutomator2** y **ADB** desde un contenedor Docker.

## 📋 Requisitos

- Docker instalado
- Dispositivo Android con:
  - Depuración USB habilitada
  - Conectado por USB al ordenador
  - Modo de desarrollador activado

## 🚀 Construcción de la Imagen

```bash
docker build -t uiautomator2-test .
```

## 🔧 Uso

### En macOS

```bash
docker run --rm -it \
  --privileged \
  -v /var/run:/var/run \
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

### Permisos USB en macOS

En macOS, el acceso a dispositivos USB desde Docker puede ser complejo. Alternativas:

1. **Usar ADB sobre TCP/IP** (Recomendado para macOS):
   ```bash
   # En tu máquina host, conecta el dispositivo y ejecuta:
   adb tcpip 5555
   adb connect <IP_DEL_DISPOSITIVO>:5555
   
   # Luego ejecuta el contenedor con acceso a la red del host:
   docker run --rm -it --network host uiautomator2-test
   ```

2. **Modificar el script para conexión TCP**:
   ```python
   # En test_device.py, cambia la línea de conexión a:
   d = u2.connect('<IP_DEL_DISPOSITIVO>:5555')
   ```

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
├── Dockerfile          # Configuración del contenedor
├── requirements.txt    # Dependencias Python
├── test_device.py      # Script de prueba
└── README.md          # Este archivo
```

## 🔗 Enlaces Útiles

- [UIAutomator2 Documentation](https://github.com/openatx/uiautomator2)
- [ADB Documentation](https://developer.android.com/tools/adb)
- [Docker Documentation](https://docs.docker.com/)

## 📄 Licencia

MIT

