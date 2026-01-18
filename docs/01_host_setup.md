# 01. Configuración del Host (Yocto Project)

Esta guía detalla exhaustivamente cómo preparar tu estación de trabajo (Host) para compilar distribuciones Linux personalizadas usando Yocto Project (versión Kirkstone) para la Xilinx Kria KV260.

## 1. Requisitos del Sistema Host

Para una compilación exitosa y eficiente, tu PC debe cumplir con los siguientes requisitos:

*   **Sistema Operativo:** Ubuntu 22.04 LTS (Jammy Jellyfish).


## 2. Instalación de Dependencias (Ubuntu 22.04 LTS)


```bash
sudo apt update && sudo apt upgrade -y
```

### Paquetes Esenciales para Yocto Project
Estos son los paquetes requeridos por la documentación oficial de Yocto para Kirkstone:

```bash
sudo apt install -y gawk wget git diffstat unzip texinfo gcc build-essential \
     chrpath socat cpio python3 python3-pip python3-pexpect xz-utils \
     debianutils iputils-ping python3-git python3-jinja2 libegl1-mesa \
     libsdl1.2-dev pylint3 xterm zstd liblz4-tool lz4 file locales
```


```bash
sudo apt install -y python-is-python3
```

## 3. Preparación del Directorio de Trabajo

Es una buena práctica mantener ordenado el entorno de desarrollo y separar las capas (layers) de los directorios de compilación.

Usaremos `/home/alvaro/yocto` como directorio base.

```bash
mkdir -p /home/alvaro/yocto/layers
mkdir -p /home/alvaro/yocto/downloads
mkdir -p /home/alvaro/yocto/sstate-cache
```


## 4. Layers usadas


### 4.1. Poky (El motor de Yocto)
```bash
git clone -b kirkstone git://git.yoctoproject.org/poky
```

### 4.2. Dependencias OpenEmbedded
Muchas recetas dependen de librerías comunes (Python, Networking, etc.).
```bash
git clone -b kirkstone git://git.openembedded.org/meta-openembedded
```

### 4.3. Meta-Xilinx (BSP Oficial)
Provee soporte para el hardware ZynqMP y configuraciones base.
```bash
git clone -b kirkstone-next https://github.com/Xilinx/meta-xilinx.git
git clone -b kirkstone-next https://github.com/Xilinx/meta-xilinx-tools.git
```

### 4.4. Meta-Kria (Específico SOM)
Contiene las configuraciones específicas para los SoM K26 y las carrier cards (KV260, KR260).
```bash
git clone -b rel-v2022.1 https://github.com/Xilinx/meta-kria.git
```

### 4.5. Meta-Intel-RealSense (Cámaras 3D)
Provee las recetas para `librealsense2` y SDKs relacionados.
```bash
git clone -b kirkstone https://github.com/IntelRealSense/meta-intel-realsense.git
```
