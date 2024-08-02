# pyffscreenrecorder
Capture and record your screen with ffmpeg ussing this Python GUI

# Dependencies

```
sudo apt install ffmpeg python3-tk tk-dev python3-psutil
```



## Features

- Record the screen in a rectangle of 854x480 with follow mouse, this rectangle can be moved around the screen to capture what matters most to you

  ## 

# Installation

I suggest that you clone this project in a special folder

```
git clone https://github.com/wachin/ffmpeg-screencast
```



## Screencast





## Join videos (Status not impremented yet)

The join the videos get on top of the script:

→ join-mkv.sh

the videos will be joined into the folder:

🗀 recorded-videos

if for some reason you need the initial videos they will be in the folder:

🗀 Old

script to joind the videos:

```
./join-mkv.sh 
```



**Other FFmpeg options** I have made this program so that it records with the videos in the mkv format because it gave me the best results, but you can record with mp4 by copying some of the profiles that are in the folder:

🗀 Profiles

where there are also profiles to record in full screen, example:

[![img](https://github.com/wachin/ffmpeg-screencast/raw/main/vx_images/570244321122966.png)](https://github.com/wachin/ffmpeg-screencast/blob/main/vx_images/570244321122966.png)

and that is:

[![img](https://github.com/wachin/ffmpeg-screencast/raw/main/vx_images/315614269937310.png)](https://github.com/wachin/ffmpeg-screencast/blob/main/vx_images/315614269937310.png)

then run clex in a terminal in the main path and see:

[![img](https://github.com/wachin/ffmpeg-screencast/raw/main/vx_images/115894179807496.png)](https://github.com/wachin/ffmpeg-screencast/blob/main/vx_images/115894179807496.png)

hit Enter end the recorder are into the full screen

# The beggining



First I started doing some tutorials on how to record the screen with ffmpeg from the terminal. In Spanish:

**[Screencast] Grabar pantalla con FFmpeg 4.2 + seguir cursor + mostrar cursor + grabar rectangulo de 480p** <https://facilitarelsoftwarelibre.blogspot.com/2021/03/screencast-ffmpeg-follow-mouse-linux.html>