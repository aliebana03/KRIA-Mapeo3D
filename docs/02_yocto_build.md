# 02. Guía de Compilación (Bitbake)

Esta sección cubre la creación, configuración y compilación del proyecto Yocto para generar una imagen de sistema operativo completa y funcional para la Kria KV260.


## 1. Inicialización del Entorno

Cargar las variables de entorno.

```bash
cd /home/alvaro/yocto
# El directorio de compilación por defecto suele ser 'build'
source layers/poky/oe-init-build-env build
```

## 2. Configuración (`conf/local.conf`)

El archivo de local.conf y bblayer.conf se encuentran en la carpeta docs/

## 3. Proceso de Compilación

```bash
# Limpiar caché de artefactos de arranque
bitbake -c cleansstate device-tree u-boot-xlnx linux-xlnx u-boot-zynq-scr
```

### Paso 2: Compilar Imagen
Lanza la compilación de la imagen de escritorio (Sato).

```bash
bitbake core-image-sato
```


### Paso 3: Localizar el Resultado
Al finalizar, la imagen se encuentra en:
`tmp/deploy/images/kv260-starter-kit/`

Busca el archivo con extensión **`.wic`**.
