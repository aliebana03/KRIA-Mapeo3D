# 03. Instalación y Setup de Kria KV260

Guía detallada para transferir la imagen generada a la tarjeta SD, configurar el arranque y preparar el hardware para el Mapeo 3D.

## 1. Flasheo de la Tarjeta SD

Necesitarás una tarjeta microSD de **8GB** o **16GB** (La imagen de este proyecto ocupó alrededor de 4 GB).

## Desde Windows (BalenaEtcher)

1.  Copia el archivo `.wic` a Windows.
2.  Descarga e instala [BalenaEtcher].
3.  Etcher soporta archivos comprimidos directamente. Selecciona el archivo y la tarjeta SD, y pulsa "Flash".



## 2. Boot y Primer Inicio

### 2.1. Conexiones Físicas
1.  Inserta la SD en la ranura de la Kria KV260.
2.  Conecta tu cámara **Intel RealSense D435i** a uno de los puertos **USB 3.0** (los azules).
3.  Conecta un cable Micro-USB desde el puerto **JTAG/UART** de la Kria a tu PC.
4.  Conecta la fuente de alimentación (12V/3A).

### 2.2. Terminal Serial
Abre una terminal serial en tu PC para ver el log de arranque.
*   **Linux:** `sudo screen /dev/ttyUSB1 115200`
*   **Windows:** Putty -> Serial -> COMx -> 115200.

Deberías ver el arranque de U-Boot seguido del Kernel Linux.

### 2.3. Login
Por defecto en las imágenes de desarrollo Yocto (`debug-tweaks` activado en `local.conf`):
*   **Usuario:** `root`
*   **Contraseña:** (Vacío, presionar Enter).


## 3. Configuración Post-Instalación

### 3.1. Verificación de Periféricos

#### Cámara RealSense (USB 3.0 Check)
Es crucial verificar que la cámara se ha negociado como SuperSpeed (USB 3.0).

```bash
lsusb -t
```
Salida esperada para Intel RealSense:
```
/:  Bus 02.Port 1: Dev 1, Class=root_hub, Driver=xhci-hcd/4p, 5000M
    |__ Port 1: Dev 2, If 0, Class=Video, Driver=uvcvideo, 5000M
```
