#!/bin/bash

set -x

# Obtener las dimensiones de la pantalla
SCREEN_WIDTH=$(xdpyinfo | awk '/dimensions/{print $2}' | cut -d'x' -f1)
SCREEN_HEIGHT=$(xdpyinfo | awk '/dimensions/{print $2}' | cut -d'x' -f2)

# Calcular las coordenadas para centrar la ventana de grabación
X_OFFSET=$((($SCREEN_WIDTH - 854) / 2))
Y_OFFSET=$((($SCREEN_HEIGHT - 480) / 2))

ffmpeg -follow_mouse 50 -show_region 1 -video_size 854x480 -framerate 30 -f x11grab -i :0.0+$X_OFFSET,$Y_OFFSET \
       -f alsa -ac 2 -i default \
       -c:v libx264rgb -crf 0 -preset ultrafast \
       "./Out-$(date '+%Y-%m-%d_%H.%M.%S').mp4"
