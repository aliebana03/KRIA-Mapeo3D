# KRIA KV260 3D Mapping Project

Sistema de escaneo y mapeo 3D utilizando **Xilinx Kria KV260** e **Intel RealSense D435i**.

Este proyecto ha sido migrado a **Python**.

## Características
- **Captura 3D:** Adquisición de nubes de puntos RGB-D en tiempo real.
- **Python Core:** Lógica implementada totalmente en Python usando `pyrealsense2` y `numpy`.
- **Flexible OS:** Compatible con imágenes Yocto Kirkstone o PetaLinux 2022.x.
- **Exportación:** Guardado de archivos `.ply` compatibles con MeshLab/CloudCompare.
- **Documentación Completa:** Todo el código fuente está comentado en **Español**.

## Detalles del Proyecto Yocto
Este sistema ha sido compilado utilizando **Yocto Project (Kirkstone LTS)** con las siguientes capas y configuraciones:

### Capas (Layers)
*   **poky (meta, meta-poky):** Base del sistema Yocto.
*   **meta-xilinx (meta-xilinx-core, meta-xilinx-bsp):** Soporte oficial para hardware Xilinx.
*   **meta-xilinx-tools:** Herramientas adicionales (xsct, etc.).
*   **meta-kria:** Soporte específico para las placas Kria (KV260).
*   **meta-intel-realsense:** Drivers y librerías para cámaras RealSense (`librealsense2`).
*   **meta-openembedded:** Dependencias varias (`meta-oe`, `meta-python`).

### Configuración (local.conf)
*   **Propocionado en docs/:** 

## Estructura de Documentación (`docs/`)

### Guía Principal
Usa estos archivos si quieres construir una distribución Linux personalizada desde cero.
Ubicación: `docs/yocto/`
- `01_host_setup.md`: Prep del PC Host.
- `02_yocto_build.md`: Compilación de la imagen con Bitbake.
- `03_kria_setup.md`: Setup de hardware.
- `04_user_manual.md`: Uso de la app.


## Estructura del Código
```
├── src/                    # Código Fuente Python
│   ├── main.py             # App principal
│   ├── camera.py           # Driver RealSense
│   └── mapping.py          # Lógica de nube de puntos
└── scripts/
    └── run_mapping.sh      # Launcher
```

## Inicio Rápido

1.  **Preparar Hardware:** Conecta la Kria KV260 y la cámara D435i (USB 3.0).
2.  **Ejecutar:**
    ```bash
    ./scripts/run_mapping.sh
    ```
3.  **Controles:**
    - `S`: Guardar nube de puntos.
    - `Q`: Salir.
