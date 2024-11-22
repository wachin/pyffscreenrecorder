#!/bin/bash

set -x

# Obtener las dimensiones de la pantalla con xdpyinfo del paquete x11-utils
SCREEN_WIDTH=$(xdpyinfo | awk '/dimensions/{print $2}' | cut -d'x' -f1)
SCREEN_HEIGHT=$(xdpyinfo | awk '/dimensions/{print $2}' | cut -d'x' -f2)

# Calcula las coordenadas para centrar la ventana de grabación de 854x480 en tu pantalla.
X_OFFSET=$((($SCREEN_WIDTH - 854) / 2))
Y_OFFSET=$((($SCREEN_HEIGHT - 480) / 2))

# Usa estas coordenadas calculadas en el comando -i de FFmpeg.
ffmpeg -follow_mouse 50 -show_region 1 -video_size 854x480 -framerate 30 -f x11grab -i :0.0+$X_OFFSET,$Y_OFFSET \
       -f alsa -ac 2 -i default \
       -c:v libx264 -crf 23 -preset veryfast \
       "./Out-$(date '+%Y-%m-%d_%H.%M.%S').mp4"

# Cambios hechos
# El códec libx264rgb genera archivos con una calidad extremadamente alta (sin pérdida), pero es muy intensivo en recursos. 
# Códec de video: -c:v libx264 en lugar de libx264rgb. Esto ahorra muchos recursos al no hacer la codificación en formato RGB, que es más pesado, tendrá un buen equilibrio entre calidad y rendimiento.
# CRF: Cambiado el valor de -crf a 23 en lugar de 0. Este es el valor predeterminado de FFmpeg para una calidad visual razonable sin que consuma tanto CPU.
# Preset: Cambio de ultrafast por veryfast. Esto debería hacer que la codificación sea más eficiente sin ser tan demandante.
