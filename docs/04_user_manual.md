# 04. Manual de Usuario: Aplicación de Mapeo 3D

Este documento describe cómo desplegar, ejecutar y operar la aplicación de Mapeo 3D en la Kria KV260 una vez que el sistema operativo está instalado.

## 1. Despliegue del Software

Dado que la imagen del sistema operativo es nueva, necesitas copiar el código de la aplicación (Python) a la placa.

### Método A: Copia vía SCP 
Desde tu PC Host (Windows), abre **PowerShell** y sigue este bloque completo paso a paso:

```powershell

# 2. Crear carpetas destino en la Kria
ssh root@192.168.1.25 "mkdir -p ~/kria_mapping/scripts ~/kria_mapping/exports"

# 3. Copiar código y reglas (importante copiar también el archivo .rules)
scp -r src scripts root@192.168.1.25:~/kria_mapping/
scp scripts/99-realsense-libusb.rules root@192.168.1.25:/etc/udev/rules.d/

# 4. Aplicar permisos (y borrar reglas conflictivas del sistema)
ssh root@192.168.1.25 "rm -f /etc/udev/rules.d/99-librealsense2-libusb.rules"
ssh root@192.168.1.25 "udevadm control --reload-rules && udevadm trigger"
```

## 2. Ejecución de la Aplicación

La aplicación cuenta con un script lanzador (`run_mapping.sh`) que configura el entorno necesario.

1.  Accede al directorio:
    ```bash
    cd /home/root/kria_mapping/scripts
    ```

2.  Da permisos de ejecución (primera vez):
    ```bash
    chmod +x run_mapping.sh
    ```

3.  Ejecuta:
    ```bash
    ./run_mapping.sh
    ```

### Opciones de Lanzamiento
El script wrapper acepta argumentos directos para la aplicación Python:

| Argumento | Descripción | Ejemplo |
|-----------|-------------|---------|
| `--headless` | Ejecuta sin interfaz gráfica (útil para SSH/Log). | `./run_mapping.sh --headless` |
| `--width` | Ancho resolución cámara. | `./run_mapping.sh --width 1280` |
| `--height` | Alto resolución cámara. | `./run_mapping.sh --height 720` |
| `--fps` | Fotogramas por segundo (15, 30, 60). | `./run_mapping.sh --fps 15` |

### Ejecución con Monitor (HDMI)
Si conectas un monitor HDMI, puedes ver la imagen en tiempo real y la nube de puntos.
1.  Conecta el HDMI **antes** de encender la Kria.
2.  Si lanzas el comando desde el Puerto Serie o SSH, debes indicar dónde mostrar la ventana:
    ```bash
    export DISPLAY=:0
    ./run_mapping.sh
    ```
    *(Nota: No uses `--headless` en este caso).*

## 3. Interfaz y Controles

Si ejecutas con monitor conectado (modo gráfico), verás una ventana dividida con la imagen RGB y el mapa de profundidad.

### Teclas de Control
La ventana debe tener el foco para recibir comandos.

*   **[Q] o [ESC]:** **Salir**. Cierra la conexión con la cámara y termina el programa limpiamente.
*   **[S]:** **Guardar**. Genera una nube de puntos instantánea.
    *   *Feedback:* Verás un mensaje en consola `[Export] Saving to...`.
    *   *Ubicación:* Carpeta `exports/` en el directorio del proyecto.
*   **[P]:** **Pausa**. Congela la visualización (la cámara sigue activa en background). Útil para inspeccionar un frame.
*   **[F]:** **Filtros**. Activa/Desactiva los filtros de post-procesado (Decimation, Spatial, Temporal).
    *   *Uso:* Si la imagen 3D tiene mucho ruido o "agujeros", activa los filtros. Si notas lag, desactívalos.

