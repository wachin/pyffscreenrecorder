#!/bin/bash

set -x

ffmpeg -follow_mouse 50 -show_region 1 -video_size 854x480 -f 30 -f x11grab -i :0.0+200,150  \
       -f alsa -ac 2 -i default  \
       -c:v libx264rgb -crf 0 -preset ultrafast \
       "./Out-$(date '+%Y-%m-%d_%H.%M.%S').mp4"
